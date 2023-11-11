import {Ref, ref} from "vue";
import * as database from "firebase/database";
import algoliasearch from "algoliasearch";

import {useAppStore} from "./store/app";
import {Song} from "@/@types/global/song";
import Songs from "@/songs.json";


export type Playlist = {
  title: string;
  description: string;
  songs: string[];
}

export const ALGOLIA_APP_ID = "6T9A9U650D";
export const ALGOLIA_SEARCH_KEY = "fe209ec7af26fc0524f5ef8f9adc340b";
export const ALGOLIA_SEARCH_INDEX = "songs";

const algoliaClient = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_SEARCH_KEY);
export const algoliaIndex = algoliaClient.initIndex(ALGOLIA_SEARCH_INDEX)

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
      privatePlaylists.value = null;
      if (privatePlaylistUnsubscribe !== null) {
        privatePlaylistUnsubscribe();
        privatePlaylistUnsubscribe = null;
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

export function addToFavorite(songUUID: string) {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (favoriteSongs.value.has(songUUID)) {
    return;
  }
  const db = database.getDatabase();
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...favoriteSongs.value, songUUID]
  );
};

export function removeFromFavorite(songUUID: string) {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (!favoriteSongs.value.has(songUUID)) {
    return;
  }
  const db = database.getDatabase();
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...(favoriteSongs.value || [])].filter(v => v !== songUUID)
  );
};
