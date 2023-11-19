
<script lang="ts" setup>
import {useRoute} from "vue-router";
import type {Song} from "@/@types/global/song.d.ts";
import {addToFavorite, algoliaIndex, favoriteSongs, removeFromFavorite, removePlayList} from "@/common";
import {ObjectWithObjectID} from "@algolia/client-search";
import {onMounted, Ref, ref} from "vue";
import PlaylistSongCard from "@/components/PlaylistSongCard.vue";

const route = useRoute();

let {playlistId: queryPlaylistId} = route.params;
const playlistId = queryPlaylistId as string;

console.debug(history.state);
console.debug(route.state);

const {songs: querySongs, visibility: queryVisibility, title, description} = route.query;
const visibility = queryVisibility as "public" | "private";

let songs: string[] = [];
if (Array.isArray(querySongs)) {
  songs = querySongs.filter<string>((song): song is string => typeof song === "string");
} else {
  if (typeof querySongs === "string") {
    songs = [querySongs];
  } else {
    songs = [];
  }
}

let playlistSongs: ({uuid: string} & Song)[] | null = null;
onMounted(async () => {
  const searchSongs = await algoliaIndex.getObjects<Song>(songs);
  playlistSongs = searchSongs.results
    .filter((song): song is Song & ObjectWithObjectID => song !== null)
    .map(({objectID, ...song}) => ({uuid: objectID, ...song}));
});

</script>

<template>
  <v-container>
    <v-card>
      <v-col>
        <v-card-title>
          {{ title }}
        </v-card-title>
        <v-card-subtitle>
          {{ description }}
        </v-card-subtitle>
      </v-col>
      <v-col>
        <v-btn class="mx-1" :icon="true" elevation="1">
          <v-icon icon="mdi-play" />
        </v-btn>
        <v-btn class="mx-1" :icon="true" elevation="1">
          <v-icon icon="mdi-shuffle" />
        </v-btn>
      </v-col>
      <v-col>
        <template v-for="({uuid, ...song}, index) in playlistSongs" :key="uuid">
          <!-- <v-lazy :min-height="30" :options="{threshold: 0.5}" transition="fade-transition"> -->
          <PlaylistSongCard v-bind="{
            ...song,
            isFavorite: favoriteSongs?.has(uuid) ?? null,
            isFull: song.length === 'full',
            visibility,
            playlistId,
            playlist: playlistSongs!,
            playlistIndex: index,
          }" @add-favorite="addToFavorite" @remove-favorite="removeFromFavorite" />
          <!-- </v-lazy> -->
        </template>
      </v-col>
    </v-card>
  </v-container>
</template>
