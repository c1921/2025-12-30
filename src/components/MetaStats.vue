<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { foodStock, aliveNpcCount } = useGameState();
</script>

<template>
  <div class="flex flex-row gap-4.5">
    <div
      class="flex flex-1 items-center justify-between rounded-2xl bg-base-200 px-4 py-3 font-semibold text-base-content/80"
    >
      <span>Food Stock</span>
      <strong class="text-xl text-base-content">{{ foodStock }}</strong>
    </div>
    <div
      class="flex flex-1 items-center justify-between rounded-2xl bg-base-200 px-4 py-3 font-semibold text-base-content/80"
    >
      <span>NPCs</span>
      <strong class="text-xl text-base-content">{{ aliveNpcCount }}</strong>
    </div>
  </div>
</template>
