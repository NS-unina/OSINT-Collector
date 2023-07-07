const osint = require("./osint");

// Informazioni principali del profilo Target:
//osint.userInfo("curiosity_astronomy");

// Lista degli utenti seguiti dal Target:
//osint.userFollowing("curiosity_astronomy", 2);

// Lista degli utenti che seguono il Target:
//osint.userFollowers("curiosity_astronomy", 2);

// Lista delle descrizioni dei primi "count" post nel feed del Target:
osint.userFeedText("curiosity_astronomy", 2)