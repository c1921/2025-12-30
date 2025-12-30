<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { speed, isRunning, isResetting, setSpeed, toggleRunning, resetState } =
  useGameState();
</script>

<template>
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
</template>

<style scoped>
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

@media (max-width: 640px) {
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
