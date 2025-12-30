<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { day } = useGameState();
</script>

<template>
  <div class="day">
    Day <span>{{ day }}</span>
  </div>
</template>

<style scoped>
.day {
  font-size: 42px;
  font-weight: 700;
  color: #0b1b33;
}

.day span {
  font-size: 56px;
  color: #e26b49;
}
</style>
