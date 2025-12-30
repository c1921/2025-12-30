<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { invoke } from "@tauri-apps/api/core";

const day = ref(0);
const speed = ref(1);
const isRunning = ref(true);
const isTicking = ref(false);
const errorMsg = ref("");

let timer: number | undefined;

async function advanceDay() {
  if (isTicking.value) return;
  isTicking.value = true;
  errorMsg.value = "";
  try {
    day.value = await invoke<number>("tick_day", { multiplier: 1 });
  } catch (err) {
    errorMsg.value = String(err);
  } finally {
    isTicking.value = false;
  }
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

onMounted(() => {
  if (isRunning.value) {
    startTimer();
  }
});

onBeforeUnmount(() => {
  stopTimer();
});
</script>

<template>
  <main class="shell">
    <section class="panel">
      <div class="day">
        Day <span>{{ day }}</span>
      </div>
      <div class="controls">
        <div class="speed">
          <button :class="{ active: speed === 1 }" @click="setSpeed(1)">
            1x
          </button>
          <button :class="{ active: speed === 5 }" @click="setSpeed(5)">
            5x
          </button>
          <button :class="{ active: speed === 10 }" @click="setSpeed(10)">
            10x
          </button>
        </div>
        <button class="toggle" @click="toggleRunning">
          {{ isRunning ? "Pause" : "Resume" }}
        </button>
      </div>
      <p class="hint">Speed changes tick interval from 1000ms to 200ms or 100ms.</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </section>
  </main>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap");

:root {
  font-family: "Space Grotesk", "Noto Sans", sans-serif;
  font-size: 16px;
  line-height: 1.5;
  font-weight: 400;
  color: #0b1020;
  background-color: #f4f3ef;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at top, #f7e6d3, #e7eaf4 55%, #f1f1f1);
}

.shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px;
}

.panel {
  width: min(520px, 92vw);
  padding: 32px;
  border-radius: 28px;
  background: #ffffffcc;
  box-shadow: 0 30px 80px rgba(12, 16, 34, 0.15);
  backdrop-filter: blur(18px);
  display: grid;
  gap: 18px;
}

.day {
  font-size: 42px;
  font-weight: 700;
  color: #0b1b33;
}

.day span {
  font-size: 56px;
  color: #e26b49;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: center;
}

.speed {
  display: flex;
  gap: 10px;
}

button {
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-size: 16px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  background: #f2f3fb;
  color: #25223a;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(37, 34, 58, 0.18);
}

button.active {
  background: #0b1b33;
  color: #fff5ea;
}

.toggle {
  background: #e26b49;
  color: #fff5ea;
  padding: 10px 22px;
}

.hint {
  margin: 0;
  font-size: 14px;
  color: #5c5a6b;
}

.error {
  margin: 0;
  padding: 10px 12px;
  border-radius: 12px;
  background: #ffebe8;
  color: #b12a28;
  font-size: 13px;
  word-break: break-word;
}

@media (max-width: 640px) {
  .panel {
    padding: 24px;
  }

  .controls {
    flex-direction: column;
    align-items: stretch;
  }

  .speed {
    justify-content: center;
  }

  .toggle {
    width: 100%;
  }
}
</style>
