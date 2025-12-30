<script setup lang="ts">
import { onBeforeUnmount, onMounted } from "vue";
import { useGameState } from "../composables/useGameState";

const { initialize, stopTimer } = useGameState();

onMounted(() => {
  initialize();
});

onBeforeUnmount(() => {
  stopTimer();
});
</script>

<template>
  <span class="game-controller" aria-hidden="true"></span>
</template>

<style scoped>
.game-controller {
  display: none;
}
</style>
