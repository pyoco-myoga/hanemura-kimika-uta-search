
<script lang="ts" setup>
import type {Song} from "@/@types/global/song.d.ts";
import {addToFavorite, algoliaIndex, favoriteSongs, removeFromFavorite, playPlaylist, playPlaylistRandom} from "@/common";
import {ObjectWithObjectID} from "@algolia/client-search";
import {onBeforeMount} from "vue";
import PlaylistSongCard from "@/components/PlaylistSongCard.vue";
import {ref} from "vue";
import {Ref} from "vue";

const show = defineModel<boolean>();

const props = defineProps<{
  title: string,
  description: string,
  visibility: "public" | "private"
  playlistId: string,
  songs: string[],
}>();

let playlistSongs: Ref<({uuid: string} & Song)[] | null> = ref(null);

onBeforeMount(async () => {
  const searchSongs = await algoliaIndex.getObjects<Song>(props.songs);
  playlistSongs.value = searchSongs.results
    .filter((song): song is Song & ObjectWithObjectID => song !== null)
    .map(({objectID, ...song}) => ({uuid: objectID, ...song}));
});

</script>

<template>
  <v-bottom-sheet v-model="show" inset>
    <v-card>
      <v-col>
        <div class="text-end">
          <v-btn icon="mdi-close" elevation="0" @click="show = false"/>
        </div>
        <v-card-title>
          {{ title }}
        </v-card-title>
        <v-card-subtitle>
          {{ description }}
        </v-card-subtitle>
      </v-col>
      <v-col>
      </v-col>
      <v-col>
        <v-btn class="mx-1" icon="mdi-play" elevation="1" @click="playPlaylist(songs)" />
        <v-btn class="mx-1" icon="mdi-shuffle" elevation="1" @click="playPlaylistRandom(songs)" />
      </v-col>
      <v-col>
        <template v-if="playlistSongs === null">
          <div class="text-center">
            <v-progress-circular indeterminate />
          </div>
        </template>
        <template v-else-if="playlistSongs.length === 0">
          <div class="text-center">
            曲はありません
          </div>
        </template>
        <template v-else>
          <template v-for="({uuid, ...song}, index) in playlistSongs" :key="uuid">
            <v-lazy :min-height="30" :options="{threshold: 0.5}" transition="fade-transition">
              <PlaylistSongCard v-bind="{
                ...song,
                isFavorite: favoriteSongs?.has(uuid) ?? null,
                isFull: song.length === 'full',
                visibility,
                playlistId,
                playlist: playlistSongs!,
                playlistIndex: index,
              }" @add-favorite="addToFavorite" @remove-favorite="removeFromFavorite" />
            </v-lazy>
          </template>
        </template>
      </v-col>
    </v-card>
  </v-bottom-sheet>
</template>
