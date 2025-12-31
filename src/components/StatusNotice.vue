<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { errorMsg } = useGameState();
</script>

<template>
  <p v-if="errorMsg" class="alert alert-error py-2 text-xs">
    {{ errorMsg }}
  </p>
</template>
