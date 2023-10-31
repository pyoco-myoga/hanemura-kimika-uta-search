<template>
  <router-view />
</template>

<script lang="ts" setup>
import {storeSubscribe, publicPlaylistsSubscribe} from "@/common";
storeSubscribe();
publicPlaylistsSubscribe();
</script>
