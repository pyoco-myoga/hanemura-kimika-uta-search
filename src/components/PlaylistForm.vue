<script lang="ts" setup>
import {ref} from 'vue';
import * as database from "firebase/database";
import {uidRef} from '@/common';
import {v4 as uuidv4} from 'uuid';

const show = defineModel<boolean>({required: true});

const props = defineProps<{
  playlistId?: string;
  title?: string;
  description?: string;
  isPublic?: boolean;
}>();

const playlistId = ref(props.playlistId ?? uuidv4());
const title = ref(props.title ?? "");
const description = ref(props.description ?? "");
const isPublic = ref(props.isPublic ?? false);

const db = database.getDatabase();
const addOrUpdatePlayList = async () => {
  try {
    await database.set(
      database.ref(db, `users/${uidRef.value}/playlists/${playlistId.value}`),
      {
        "title": title.value,
        "description": description.value,
        "songs": []
      }
    );
    if (isPublic.value) {
      await database.set(
        database.ref(db, `public_playlists/${playlistId.value}`), {
        "uid": uidRef.value
      });
    }
  } catch (e) {
    console.log(e);
  }
};
</script>

<template>
  <v-dialog v-model="show" width="80%">
    <v-card>
      <v-text-field v-model="title" label="タイトル" />
      <v-textarea v-model="description" label="概要" />
      <v-switch color="primary" v-model="isPublic">
        <template v-slot:label>
          <span :class="isPublic ? 'text-black' : 'text-grey-darken-3'">公開する</span>
          <!-- <span class="black">公開する</span> -->
        </template>
      </v-switch>
      <v-card-actions>
        <v-btn color="primary" block @click="() => {show = false; addOrUpdatePlayList()}">作成</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
