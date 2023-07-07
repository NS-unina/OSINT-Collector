![Logo](https://i.postimg.cc/d1fpxwwz/Logo-Osint-Ig.png)

# OSINT-IG | osint library for Instagram

OSINT-IG is a OSINT tool for Instagram to collect, analyze, and run reconnaissance.

## Tools and usage

The library currently offers the following functions:

```bash
  userInfo("username");               Gets the main information of the target account.

  userFollowing("username", n);       Gets the first "n" accounts followed by the Target.

  userFollowers("username", n);       Gets the first "n" accounts that follow the Target.

  userFeedText("username", n);        Gets the first "n" Target feed descriptions.
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
