<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const {
  day,
  speed,
  isRunning,
  isResetting,
  setSpeed,
  toggleRunning,
  resetState,
} = useGameState();
</script>

<template>
  <div
    class="flex flex-wrap items-center gap-3 sm:gap-4"
  >
    <div class="font-bold">
      Day <span class="text-primary">{{ day }}</span>
    </div>
    <div class="join">
      <button
        class="btn btn-sm join-item"
        :class="speed === 1 ? 'btn-primary' : ''"
        @click="setSpeed(1)"
      >
        1x
      </button>
      <button
        class="btn btn-sm join-item"
        :class="speed === 5 ? 'btn-primary' : ''"
        @click="setSpeed(5)"
      >
        5x
      </button>
      <button
        class="btn btn-sm join-item"
        :class="speed === 10 ? 'btn-primary' : ''"
        @click="setSpeed(10)"
      >
        10x
      </button>
    </div>
    <button
      class="btn btn-sm btn-square"
      :class="isRunning ? '' : 'btn-error'"
      @click="toggleRunning"
      :aria-label="isRunning ? 'Pause' : 'Resume'"
    >
      <span
        class="size-4.5 shrink-0"
        :class="isRunning ? 'icon-[tabler--player-pause]' : 'icon-[tabler--player-play]'"
      ></span>
    </button>
    <button class="btn btn-sm btn-warning" @click="resetState" :disabled="isResetting">
      {{ isResetting ? "Resetting..." : "Reset" }}
    </button>
  </div>
</template>
