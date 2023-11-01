import {Ref, ref} from "vue";
import * as database from "firebase/database";

import {useAppStore} from "./store/app";
import {Song} from "@/@types/global/song";
import Songs from "@/songs.json";


export type Playlist = {
  title: string;
  description: string;
  songs: string[];
}

export const songs = Songs.songs as {[uuid: string]: Song};

export const uidRef: Ref<string | null> = ref(null);
export const favoriteSongs: Ref<Set<string> | null> = ref(null);
export const privatePlaylists: Ref<{[playlist_id: string]: {uid: string} & Playlist} | null> = ref(null);
export const publicPlaylists: Ref<{[playlist_id: string]: {uid: string}} | null> = ref(null);

let favoriteUnsubscribe: database.Unsubscribe | null = null;
let publicPlaylistUnsubscribe: database.Unsubscribe | null = null;
let privatePlaylistUnsubscribe: database.Unsubscribe | null = null;

export const storeSubscribe = () => {
  const store = useAppStore();
  const db = database.getDatabase();
  store.$subscribe((_mutation, state) => {
    uidRef.value = state.user?.uid ?? null;

    if (uidRef.value !== null) {  // login
      favoriteUnsubscribe = database.onValue(
        database.ref(db, `users/${uidRef.value}/favorite`),
        (snapshot: database.DataSnapshot) => {
          favoriteSongs.value = new Set(snapshot.val() || []);
        },
        (error: Error) => console.log(error));

      privatePlaylistUnsubscribe = database.onValue(
        database.ref(db, `users/${uidRef.value}/playlists`),
        (snapshot: database.DataSnapshot) => {
          privatePlaylists.value = Object.fromEntries(
            Object.entries(snapshot.val() ?? {})
              .map(([playlistId, data]) => [
                playlistId as string,
                {
                  uid: uidRef.value!,
                  title: (data as any).title,
                  description: (data as any).description,
                  songs: (data as any).songs,
                }
              ]));
        },
        e => console.log(e));

    } else {  // logout
      favoriteSongs.value = null;
      if (favoriteUnsubscribe !== null) {
        favoriteUnsubscribe();
        favoriteUnsubscribe = null;
      }
    }
  });
};

export const publicPlaylistsSubscribe = () => {
  const db = database.getDatabase();
  publicPlaylistUnsubscribe = database.onValue(
    database.ref(db, "public_playlists"),
    (snapshot: database.DataSnapshot) => {
      publicPlaylists.value = snapshot.val() ?? null;
    },
    e => console.log(e));
};

