<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { errorMsg } = useGameState();
</script>

<template>
  <p class="text-sm text-base-content/70">
    Speed changes tick interval from 1000ms to 200ms or 100ms.
  </p>
  <p v-if="errorMsg" class="alert alert-error py-2 text-xs">
    {{ errorMsg }}
  </p>
</template>
