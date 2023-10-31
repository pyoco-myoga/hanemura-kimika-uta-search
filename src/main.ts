/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

import App from "./App.vue"


import {createApp} from "vue"
import {FirebaseOptions, initializeApp} from "firebase/app";
import {registerPlugins} from "@/plugins"

const firebaseConfig: FirebaseOptions = {
    apiKey: "AIzaSyCGTVUbh92BMf27oZBhGFfrjvouPOnp6Dw",
    authDomain: "hanemura-kimika-uta-search.firebaseapp.com",
    databaseURL: "https://hanemura-kimika-uta-search-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "hanemura-kimika-uta-search",
    storageBucket: "hanemura-kimika-uta-search.appspot.com",
    messagingSenderId: "557447215614",
    appId: "1:557447215614:web:3996ea78bcd27f5c77e8af",
    measurementId: "G-Q444ZBDQW0"
};
const firebaseApp = initializeApp(firebaseConfig);

const app = createApp(App);

registerPlugins(app);

app.mount("#app");
