/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

import {onRequest} from "firebase-functions/v2/https";

import * as https from "https";

const secondsInMinute = 60;
const secondsInHour = 60 * secondsInMinute;
const secondsInDay = 24 * secondsInHour;

export const getTwitterIcon = onRequest(async (req, res) => {
  const twitterIconUrl = req.query.url;
  if (twitterIconUrl === undefined || typeof twitterIconUrl !== "string") {
    res.status(400).send("Twitter icon URL is missing");
    return;
  }

  https.get(twitterIconUrl, (response) => {
    res.set("Content-Type", "image/jpeg");
    res.set("Cache-Control", `public, max-age=${2 * secondsInDay}`);
    response.pipe(res);
  });
});

