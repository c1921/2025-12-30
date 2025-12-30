import { computed, ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import type { NPC } from "../types/game";

type TickSummary = { ok: boolean; day: number; food_stock: number };
type WorldState = { day: number; food_stock: number; npcs: NPC[] };

const day = ref(0);
const foodStock = ref(0);
const npcs = ref<NPC[]>([]);
const aliveNpcCount = computed(
  () => npcs.value.filter((npc) => npc.alive).length,
);
const speed = ref(1);
const isRunning = ref(true);
const isTicking = ref(false);
const errorMsg = ref("");
const isResetting = ref(false);

let timer: number | undefined;
let initialized = false;

async function advanceDay() {
  if (isTicking.value) return;
  isTicking.value = true;
  errorMsg.value = "";
  try {
    const result = await invoke<TickSummary>("api_time_tick", { multiplier: 1 });
    day.value = result.day;
    foodStock.value = result.food_stock;
    await refreshState();
  } catch (err) {
    errorMsg.value = String(err);
  } finally {
    isTicking.value = false;
  }
}

async function refreshState() {
  const state = await invoke<WorldState>("api_state");
  day.value = state.day;
  foodStock.value = state.food_stock;
  npcs.value = Array.isArray(state.npcs) ? state.npcs : [];
}

function startTimer() {
  if (timer !== undefined) return;
  timer = window.setInterval(() => {
    advanceDay();
  }, 1000 / speed.value);
}

function stopTimer() {
  if (timer === undefined) return;
  window.clearInterval(timer);
  timer = undefined;
}

function toggleRunning() {
  isRunning.value = !isRunning.value;
  if (isRunning.value) {
    startTimer();
  } else {
    stopTimer();
  }
}

function setSpeed(value: number) {
  speed.value = value;
  if (isRunning.value) {
    stopTimer();
    startTimer();
  }
}

async function resetState() {
  if (isResetting.value) return;
  isResetting.value = true;
  errorMsg.value = "";
  try {
    await invoke("api_reset");
    await refreshState();
  } catch (err) {
    errorMsg.value = String(err);
  } finally {
    isResetting.value = false;
  }
}

async function initialize() {
  if (initialized) return;
  initialized = true;
  errorMsg.value = "";
  try {
    await refreshState();
  } catch (err) {
    errorMsg.value = String(err);
  }
  if (isRunning.value) {
    startTimer();
  }
}

export function useGameState() {
  return {
    day,
    foodStock,
    npcs,
    aliveNpcCount,
    speed,
    isRunning,
    isTicking,
    errorMsg,
    isResetting,
    advanceDay,
    refreshState,
    toggleRunning,
    setSpeed,
    resetState,
    initialize,
    stopTimer,
  };
}
