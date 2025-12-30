<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { errorMsg } = useGameState();
</script>

<template>
  <p class="hint">Speed changes tick interval from 1000ms to 200ms or 100ms.</p>
  <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
</template>

<style scoped>
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
</style>
