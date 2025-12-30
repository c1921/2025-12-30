<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { foodStock, aliveNpcCount } = useGameState();
</script>

<template>
  <div class="meta">
    <div class="stat">
      <span>Food Stock</span>
      <strong>{{ foodStock }}</strong>
    </div>
    <div class="stat">
      <span>NPCs</span>
      <strong>{{ aliveNpcCount }}</strong>
    </div>
  </div>
</template>

<style scoped>
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

@media (max-width: 640px) {
  .meta {
    flex-direction: column;
  }
}
</style>
