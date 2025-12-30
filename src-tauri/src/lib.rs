use std::fs;
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::{Mutex, OnceLock};

use serde::Serialize;
use serde_json::{json, Value};
use tauri::path::BaseDirectory;
use tauri::Manager;

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

#[cfg(target_os = "windows")]
const CREATE_NO_WINDOW: u32 = 0x08000000;

struct PythonProcess {
    child: Child,
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
    state_path: PathBuf,
}

impl PythonProcess {
    fn spawn(script_path: PathBuf, state_path: PathBuf) -> Result<Self, String> {
        let mut command = Command::new("python");
        command
            .arg("-u")
            .arg(script_path)
            .arg("--state")
            .arg(&state_path)
            .arg("--server")
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit());
        #[cfg(target_os = "windows")]
        {
            command.creation_flags(CREATE_NO_WINDOW);
        }
        let mut child = command
            .spawn()
            .map_err(|err| format!("failed to start python: {err}"))?;

        let stdin = child
            .stdin
            .take()
            .ok_or_else(|| "failed to open python stdin".to_string())?;
        let stdout = child
            .stdout
            .take()
            .ok_or_else(|| "failed to open python stdout".to_string())?;

        Ok(Self {
            child,
            stdin,
            stdout: BufReader::new(stdout),
            state_path,
        })
    }

    fn is_alive(&mut self) -> bool {
        match self.child.try_wait() {
            Ok(Some(_status)) => false,
            Ok(None) => true,
            Err(_err) => false,
        }
    }

    fn send_command(&mut self, payload: Value) -> Result<Value, String> {
        writeln!(self.stdin, "{}", payload)
            .map_err(|err| format!("failed to write to python: {err}"))?;
        self.stdin
            .flush()
            .map_err(|err| format!("failed to flush python: {err}"))?;

        let mut line = String::new();
        let bytes = self
            .stdout
            .read_line(&mut line)
            .map_err(|err| format!("failed to read python output: {err}"))?;
        if bytes == 0 {
            return Err("python process ended".to_string());
        }

        serde_json::from_str(line.trim())
            .map_err(|err| format!("invalid python output: {err}"))
    }

    fn tick(&mut self, multiplier: u32) -> Result<u64, String> {
        let response = self.send_command(json!({
            "cmd": "tick",
            "multiplier": multiplier,
        }))?;
        let response = require_ok(response)?;
        let day = response
            .get("day")
            .and_then(Value::as_u64)
            .ok_or_else(|| "missing day in python response".to_string())?;
        Ok(day)
    }

    fn get_state(&mut self) -> Result<Value, String> {
        let response = self.send_command(json!({ "cmd": "state" }))?;
        let response = require_ok(response)?;
        response
            .get("state")
            .cloned()
            .ok_or_else(|| "missing state in python response".to_string())
    }

    fn get_logs(&mut self, limit: u32) -> Result<Value, String> {
        let response = self.send_command(json!({
            "cmd": "logs",
            "limit": limit,
        }))?;
        let response = require_ok(response)?;
        response
            .get("logs")
            .cloned()
            .ok_or_else(|| "missing logs in python response".to_string())
    }

    fn reset_state(&mut self) -> Result<Value, String> {
        let response = self.send_command(json!({ "cmd": "reset" }))?;
        let response = require_ok(response)?;
        response
            .get("state")
            .cloned()
            .ok_or_else(|| "missing state in python response".to_string())
    }
}

fn python_process() -> &'static Mutex<Option<PythonProcess>> {
    static PROCESS: OnceLock<Mutex<Option<PythonProcess>>> = OnceLock::new();
    PROCESS.get_or_init(|| Mutex::new(None))
}

fn resolve_script_path(app: &tauri::AppHandle) -> Result<PathBuf, String> {
    let mut script_path = app
        .path()
        .resolve("python/main.py", BaseDirectory::Resource)
        .map_err(|err| format!("failed to resolve python script: {err}"))?;
    if !script_path.exists() {
        script_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("python")
            .join("main.py");
    }
    if !script_path.exists() {
        return Err(format!("python script not found: {}", script_path.display()));
    }
    Ok(script_path)
}

#[tauri::command]
fn tick_day(app: tauri::AppHandle, multiplier: u32) -> Result<u64, String> {
    with_python_process(app, |process| process.tick(multiplier))
}

#[derive(Serialize)]
struct TickSummary {
    ok: bool,
    day: u64,
    food_stock: i64,
}

#[tauri::command]
fn api_state(app: tauri::AppHandle) -> Result<Value, String> {
    with_python_process(app, |process| process.get_state())
}

#[tauri::command]
fn api_time_tick(app: tauri::AppHandle, multiplier: u32) -> Result<TickSummary, String> {
    let response = with_python_process(app, |process| {
        process.send_command(json!({
            "cmd": "tick",
            "multiplier": multiplier,
        }))
    })?;
    let response = require_ok(response)?;
    let day = response
        .get("day")
        .and_then(Value::as_u64)
        .ok_or_else(|| "missing day in python response".to_string())?;
    let food_stock = response
        .get("food_stock")
        .and_then(Value::as_i64)
        .ok_or_else(|| "missing food_stock in python response".to_string())?;
    Ok(TickSummary {
        ok: true,
        day,
        food_stock,
    })
}

#[tauri::command]
fn api_logs(app: tauri::AppHandle, limit: Option<u32>) -> Result<Value, String> {
    let limit = limit.unwrap_or(20);
    with_python_process(app, |process| process.get_logs(limit))
}

#[tauri::command]
fn api_reset(app: tauri::AppHandle) -> Result<Value, String> {
    with_python_process(app, |process| process.reset_state())
}

fn with_python_process<F, T>(app: tauri::AppHandle, action: F) -> Result<T, String>
where
    F: FnOnce(&mut PythonProcess) -> Result<T, String>,
{
    let app_data_dir = app
        .path()
        .app_data_dir()
        .map_err(|err| format!("failed to get app data dir: {err}"))?;
    fs::create_dir_all(&app_data_dir)
        .map_err(|err| format!("failed to create app data dir: {err}"))?;

    let state_path = app_data_dir.join("game_state.json");
    let script_path = resolve_script_path(&app)?;

    let process_lock = python_process();
    let mut guard = process_lock
        .lock()
        .map_err(|_| "python process lock poisoned".to_string())?;

    let needs_restart = match guard.as_mut() {
        Some(process) => !process.is_alive() || process.state_path != state_path,
        None => true,
    };

    if needs_restart {
        *guard = Some(PythonProcess::spawn(script_path, state_path.clone())?);
    }

    action(
        guard
            .as_mut()
            .ok_or_else(|| "python process unavailable".to_string())?,
    )
}

fn require_ok(response: Value) -> Result<Value, String> {
    if let Some(ok) = response.get("ok").and_then(Value::as_bool) {
        if ok {
            return Ok(response);
        }
        let error = response
            .get("error")
            .and_then(Value::as_str)
            .unwrap_or("python error");
        return Err(error.to_string());
    }
    Ok(response)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            tick_day,
            api_state,
            api_time_tick,
            api_logs,
            api_reset
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
