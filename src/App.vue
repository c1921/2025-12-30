<script setup lang="ts">
import { onMounted } from 'vue';
  onMounted(() => {
    setTimeout(() => window.HSStaticMethods.autoInit(), 100)
  });
import ControlsPanel from "./components/ControlsPanel.vue";
import DayHeader from "./components/DayHeader.vue";
import GameController from "./components/GameController.vue";
import MetaStats from "./components/MetaStats.vue";
import NpcList from "./components/NpcList.vue";
import StatusNotice from "./components/StatusNotice.vue";
</script>

<template>
  <main class="shell">
    <section class="panel">
      <GameController />
      <DayHeader />
      <MetaStats />
      <ControlsPanel />
      <StatusNotice />
      <NpcList />
    </section>
  </main>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap");

:root {
  font-family: "Space Grotesk", "Noto Sans", sans-serif;
  font-size: 16px;
  line-height: 1.5;
  font-weight: 400;
  color: #0b1020;
  background-color: #f4f3ef;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at top, #f7e6d3, #e7eaf4 55%, #f1f1f1);
}

.shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px;
}

.panel {
  width: min(520px, 92vw);
  padding: 32px;
  border-radius: 28px;
  background: #ffffffcc;
  box-shadow: 0 30px 80px rgba(12, 16, 34, 0.15);
  backdrop-filter: blur(18px);
  display: grid;
  gap: 18px;
}

@media (max-width: 640px) {
  .panel {
    padding: 24px;
  }
}
</style>
