<script lang="ts" setup>
import {getYoutubeURL} from "@/common";
import {ref, watch} from "vue";
const eventFired = defineModel<boolean>();
const show = ref(false);
const props = defineProps<{
  name: string,
  artist: string,
  video: string,
  t: number
}>();

watch(eventFired, async () => {
  if (eventFired.value) {
    const youtubeURL = getYoutubeURL(props.video, props.t);
    await navigator.clipboard.writeText(`${props.name} / ${props.artist}: ${youtubeURL}`);
    show.value = true;
    eventFired.value = false;
  }
});
</script>

<template>
  <v-snackbar v-model="show" :timeout="1000">
    <div>
      クリップボードにコピーしました
    </div>
    <div>
      {{ name }} / {{ artist }}
    </div>
  </v-snackbar>
</template>
