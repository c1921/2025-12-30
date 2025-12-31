<script setup lang="ts">
import { useGameState } from "../composables/useGameState";

const { npcs } = useGameState();
</script>

<template>
  <div class="grid gap-3">
    <h3 class="text-base font-semibold text-base-content">NPC Status</h3>
    <div class="h-56 overflow-x-auto w-full">
      <table class="table-pin-rows table-pin-cols table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Job</th>
            <th>Hunger</th>
            <th>Health</th>
            <th>Mood</th>
            <th>Status</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="npc in npcs" :key="npc.id" class="row-hover">
            <td>{{ npc.name }}</td>
            <td>{{ npc.job }}</td>
            <td>{{ npc.hunger }}</td>
            <td>{{ npc.health }}</td>
            <td>{{ npc.mood }}</td>
            <td>
              <span
                class="badge text-xs"
                :class="npc.alive ? 'badge-success' : 'badge-error'"
              >
                {{ npc.alive ? "Alive" : "Dead" }}
              </span>
            </td>
            <td class="text-right">
              <button
                class="btn btn-circle btn-text btn-sm"
                aria-label="Edit NPC"
              >
                <span class="icon-[tabler--pencil] size-5"></span>
              </button>
              <button
                class="btn btn-circle btn-text btn-sm"
                aria-label="Delete NPC"
              >
                <span class="icon-[tabler--trash] size-5"></span>
              </button>
              <button
                class="btn btn-circle btn-text btn-sm"
                aria-label="More actions"
              >
                <span class="icon-[tabler--dots-vertical] size-5"></span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
