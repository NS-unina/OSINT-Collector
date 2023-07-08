![Logo](https://i.postimg.cc/d1fpxwwz/Logo-Osint-Ig.png)

# OSINT-IG | osint library for Instagram

OSINT-IG is a OSINT tool for Instagram to collect, analyze, and run reconnaissance.

## Tools and usage

The library currently offers the following functions:

```bash
  userInfo("username");                       Gets the main information of the target account.

  userFollowing("username", n, max_id);       Gets the first "n" accounts followed by the Target, max_id is for pagination.

  userFollowers("username", n, max_id);       Gets the first "n" accounts that follow the Target,max_id is for pagination.

  userFeedText("username", n);                Gets the first "n" Target feed descriptions.

  areMyFollowingScam("username", n, max_id);  Gets the first "n" accounts followed by the Target, and tell if it's a "scam" account.
```

## Informations

```bash
  userInfo("username") return:

  igUser = {
        "usernameId",
        "fullName",
        "biography",
        "bioLinks",
        "isPrivate",
        "isVerified",
        "nFollowers",
        "nFollowing",
    }
```

## Author

- Ciro Marrazzo - [@cir.marrazzo@studenti.unina.it](https://github.com/ciro-99)
