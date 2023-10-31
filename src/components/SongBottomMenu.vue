<script lang="ts" setup>
import {uidRef} from '@/common';

const props = defineProps<{
  tiles: {
    icon: string;
    color: string;
    title: string;
    click: () => void;
    requireLogin: boolean
  }[]
}>();
const show = defineModel<boolean>();
</script>

<template>
  <v-bottom-sheet v-model="show">
    <v-list>
      <v-list-item v-for="tile in tiles.filter(tile => uidRef !== null ? true : !tile.requireLogin)" :key="tile.title"
        @click="() => {show = false; tile.click();}" :title="tile.title" density="compact">
        <template v-slot:prepend>
          <v-icon :icon="tile.icon" :color="tile.color" />
        </template>
      </v-list-item>
    </v-list>
  </v-bottom-sheet>
</template>
