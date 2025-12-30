<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { invoke } from "@tauri-apps/api/core";

type TickSummary = { ok: boolean; day: number; food_stock: number };
type WorldState = { day: number; food_stock: number; npcs: NPC[] };
type NPC = {
  id: string;
  name: string;
  job: string;
  hunger: number;
  health: number;
  mood: number;
  alive: boolean;
};

const day = ref(0);
const foodStock = ref(0);
const npcs = ref<NPC[]>([]);
const speed = ref(1);
const isRunning = ref(true);
const isTicking = ref(false);
const errorMsg = ref("");
const isResetting = ref(false);

let timer: number | undefined;

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

onMounted(() => {
  refreshState().catch((err) => {
    errorMsg.value = String(err);
  });
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
      <div class="meta">
        <div class="stat">
          <span>Food Stock</span>
          <strong>{{ foodStock }}</strong>
        </div>
        <div class="stat">
          <span>NPCs</span>
          <strong>{{ npcs.length }}</strong>
        </div>
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
        <button class="reset" @click="resetState" :disabled="isResetting">
          {{ isResetting ? "Resetting..." : "Reset" }}
        </button>
      </div>
      <p class="hint">Speed changes tick interval from 1000ms to 200ms or 100ms.</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <div class="npc-list">
        <h3>NPC Status</h3>
        <div v-for="npc in npcs" :key="npc.id" class="npc-card">
          <div class="npc-name">
            <span>{{ npc.name }}</span>
            <small>{{ npc.job }}</small>
          </div>
          <div class="npc-stats">
            <span>Hunger {{ npc.hunger }}</span>
            <span>Health {{ npc.health }}</span>
            <span>Mood {{ npc.mood }}</span>
            <span :class="{ dead: !npc.alive }">
              {{ npc.alive ? "Alive" : "Dead" }}
            </span>
          </div>
        </div>
      </div>
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

.meta {
  display: flex;
  gap: 18px;
}

.stat {
  flex: 1;
  border-radius: 16px;
  padding: 12px 16px;
  background: #f8f6f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  color: #3c3b47;
}

.stat strong {
  font-size: 20px;
  color: #0b1b33;
}

.npc-list {
  display: grid;
  gap: 12px;
}

.npc-list h3 {
  margin: 8px 0 0;
  font-size: 16px;
  color: #0b1b33;
}

.npc-card {
  border-radius: 16px;
  padding: 12px 16px;
  background: #fff;
  box-shadow: 0 12px 24px rgba(12, 16, 34, 0.08);
  display: grid;
  gap: 8px;
}

.npc-name {
  display: flex;
  align-items: baseline;
  gap: 10px;
  font-weight: 600;
  color: #1c1b29;
}

.npc-name small {
  color: #777487;
  font-weight: 500;
}

.npc-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  font-size: 13px;
  color: #4b4a57;
}

.npc-stats .dead {
  color: #b12a28;
  font-weight: 600;
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

.reset {
  background: #f6d8b2;
  color: #3a2719;
  padding: 10px 22px;
}

.reset:disabled {
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: none;
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

  .meta {
    flex-direction: column;
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
