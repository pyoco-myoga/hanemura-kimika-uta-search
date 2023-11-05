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

export const getTwitterIcon = onRequest(async (req, res) => {
  const twitterIconUrl = req.query.url;
  if (twitterIconUrl === undefined || typeof twitterIconUrl !== "string") {
    res.status(400).send("Twitter icon URL is missing");
    return;
  }

  https.get(twitterIconUrl, (response) => {
    res.set("Content-Type", "image/jpeg");
    response.pipe(res);
  });
});

// Start writing functions
// https://firebase.google.com/docs/functions/typescript

// export const helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });
