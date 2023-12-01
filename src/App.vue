<template>
  <router-view />
</template>

<script lang="ts" setup>
import {storeSubscribe, publicPlaylistsSubscribe, officialPlaylistsSubscribe} from "@/common";
storeSubscribe();
publicPlaylistsSubscribe();
officialPlaylistsSubscribe();
</script>
