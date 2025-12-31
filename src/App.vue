<script setup lang="ts">
import { onBeforeUnmount, onMounted } from "vue";
import ControlsPanel from "./components/ControlsPanel.vue";
import MetaStats from "./components/MetaStats.vue";
import NpcList from "./components/NpcList.vue";
import StatusNotice from "./components/StatusNotice.vue";
import { useGameState } from "./composables/useGameState";

const { initialize, stopTimer } = useGameState();

onMounted(() => {
  setTimeout(() => window.HSStaticMethods.autoInit(), 100);
  initialize();
});

onBeforeUnmount(() => {
  stopTimer();
});
</script>

<template>
  <main>
    <section
      class="grid gap-4.5 bg-base-300 p-6">
      <ControlsPanel />
      <MetaStats />
      <StatusNotice />
      <NpcList />
    </section>
  </main>
</template>
