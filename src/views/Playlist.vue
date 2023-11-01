<script lang="ts" setup>
import {Song} from "@/@types/global/song";
import PlaylistCard from "@/components/PlaylistCard.vue";
import PlaylistForm from "@/components/PlaylistForm.vue";
import AsyncPlayListCard from "@/components/AsyncPlayListCard.vue";
import {favoriteSongs, publicPlaylists, privatePlaylists, songs, uidRef} from "@/common";
import {ref} from "vue";

const filterSongs = (allSongs: Record<string, Song>, filter: (all: Record<string, Song>, uuid: string) => boolean): (Song & {uuid: string})[] => {
  const filteredSongs = Object.keys(allSongs).reduce((result: Record<string, Song>, uuid) => {
    if (filter(allSongs, uuid)) {
      result[uuid] = allSongs[uuid];
    }
    return result;
  }, {});

  let result: (Song & {uuid: string})[] = [];
  for (const [uuid, song] of Object.entries(filteredSongs)[Symbol.iterator]()) {
    result.push({
      uuid,
      ...song
    });
  }
  return result;
}

const showPlayListForm = ref(false);
</script>

<template>
  <template v-if="favoriteSongs !== null">
    <div class="my-2" />
    <PlaylistCard playlist-title="お気に入り" playlist-description="お気に入り登録した曲リスト" visibility="public"
      :songs="filterSongs(songs, (_, uuid) => favoriteSongs?.has(uuid) ?? false)" />
  </template>

  <div class="my-2" />
  <PlaylistCard playlist-title="おすすめ" playlist-description="おすすめ曲" visibility="public"
    :songs="filterSongs(songs, (songs, uuid) => songs[uuid].recommended ?? false)" />

  <template v-if="privatePlaylists !== null"> <!-- <=> if loaded -->
    <template v-if="Object.keys(privatePlaylists).length !== 0">
      <div>private playlist</div>
    </template>
    <template v-for="(_, playlistId) of privatePlaylists" :key="playlistId">
      <div class="my-2" />
      <AsyncPlayListCard :playlist-id="playlistId as string" :uid="uidRef!" visibility="private" />
    </template>
  </template>

  <template v-if="publicPlaylists !== null"> <!-- <=> if loaded -->
    <template v-if="Object.values(publicPlaylists).filter(({uid}) => uid !== uidRef).length !== 0">
      <div>public playlist</div>
    </template>
    <template v-for="({uid}, playlistId) of publicPlaylists" :key="playlistId">
      <template v-if="uid !== uidRef">
        <div class="my-2" />
        <AsyncPlayListCard :playlist-id="playlistId as string" :uid="uid" visibility="public" />
      </template>
    </template>
  </template>

  <template v-if="uidRef !== null">
    <v-layout-item class="text-end" model-value position="bottom" size="100">
      <div class="ma-5">
        <v-btn class="mt-auto" icon="mdi-plus" size="large" elevation="8" @click="showPlayListForm = true" />
      </div>
    </v-layout-item>
    <PlaylistForm v-model="showPlayListForm" />
  </template>
</template>
