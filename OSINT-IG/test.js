const osint = require("./osint");

// Informazioni principali del profilo Target:
//osint.userInfo("ciro.marrazzo");

// Lista degli utenti seguiti dal Target: (username, count, max_id - for pagination)
osint.userFollowing("nasa", 25, 0);

// Lista degli utenti che seguono il Target:
//osint.userFollowers("curiosity_astronomy", 2);

// Lista delle descrizioni dei primi "count" post nel feed del Target:
//osint.userFeedText("curiosity_astronomy", 6)

// Lista delle "location" dei primi "count" post nel feed del Target:
//osint.userFeedLocations("ciro.marrazzo", 3)

// Restituise la lista dei primi "count" following del Target e controlla se è un profilo "scam"
//osint.areMyFollowingScam("curiosity_astronomy", 50, 0);