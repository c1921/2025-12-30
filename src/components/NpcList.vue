<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { npcs } = useGameState();
</script>

<template>
  <div class="npc-list">
    <h3>NPC Status</h3>
    <div v-for="npc in npcs" :key="npc.id" class="npc-card">
      <div class="npc-name">
        <span>{{ npc.name }}</span>
        <small>{{ npc.job }}</small>
      </div>
      <div class="npc-stats">
        <span>Hunger {{ npc.hunger }}</span>
        <span>Health {{ npc.health }}</span>
        <span>Mood {{ npc.mood }}</span>
        <span :class="{ dead: !npc.alive }">
          {{ npc.alive ? "Alive" : "Dead" }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.npc-list {
  display: grid;
  gap: 12px;
}

.npc-list h3 {
  margin: 8px 0 0;
  font-size: 16px;
  color: #0b1b33;
}

.npc-card {
  border-radius: 16px;
  padding: 12px 16px;
  background: #fff;
  box-shadow: 0 12px 24px rgba(12, 16, 34, 0.08);
  display: grid;
  gap: 8px;
}

.npc-name {
  display: flex;
  align-items: baseline;
  gap: 10px;
  font-weight: 600;
  color: #1c1b29;
}

.npc-name small {
  color: #777487;
  font-weight: 500;
}

.npc-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  font-size: 13px;
  color: #4b4a57;
}

.npc-stats .dead {
  color: #b12a28;
  font-weight: 600;
}
</style>
