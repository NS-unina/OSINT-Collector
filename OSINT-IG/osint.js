const fetch = (...args) =>
  import('node-fetch').then(({ default: fetch }) => fetch(...args));

exports.userInfo = (username) => {
  fetch('https://i.instagram.com/api/v1/users/web_profile_info/?username=' + username, {
  method: 'GET',
  headers: {
    'Content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
  },
})
  // Parse JSON data
  .then((response) => response.json())
  
  // Showing response
  .then((json) => {
    const biography = json.data.user.biography;
    const fullName = json.data.user.full_name;
    usernameId = json.data.user.id;
    const nFollowers = json.data.user.edge_followed_by.count;
    const nFollowing = json.data.user.edge_follow.count;
    const bioLinks = [];
    json.data.user.bio_links.forEach(element => {
      bioLinks.push(element.url)
    });
    const isPrivate = json.data.user.is_private;
    const isVerified = json.data.user.is_verified;
    const igUser = {
        "usernameId": usernameId,
        "fullName": fullName,
        "biography": biography,
        "bioLinks": bioLinks,
        "isPrivate": isPrivate,
        "isVerified": isVerified,
        "nFollowers": nFollowers,
        "nFollowing": nFollowing,
    }
    console.log(igUser)

  }).catch((err) => console.log(err))
}

exports.userFollowing = (username, count) => {
  fetch('https://i.instagram.com/api/v1/users/web_profile_info/?username=' + username, {
  method: 'GET',
  headers: {
    'Content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
  },
})
  .then((response) => response.json())
  .then((json) => {
    const usernameId = json.data.user.id;

    //returning "count" number of following accounts
    fetch('  https://www.instagram.com/api/v1/friendships/' + usernameId + '/following/?count=' + count, {
    method: 'GET',
    headers: {
        'Content-type': 'application/json',
        'cookie': 'mid=ZKb90AAEAAHeJHFiThh3YHbtXxFj; ig_did=E1C82320-9298-44E8-AC11-0B73FD6F2A4B; csrftoken=8jpjVzXIehbiWFoXmJWtWVDV1KqA4gf4; ds_user_id=60150778235; sessionid=60150778235%3A1mkfoRdfeVMIfV%3A27%3AAYfcGNpKvqJ0XqWyTKU1doUREaFBvdK2nWSu-qKrEA; dpr=2.200000047683716; rur="CLN\x2c5460150778235\x2c541720202385:01f7588c3129eb9765ff944a46f68d000cc6030e5acb76cbc4f81d0fad5933a3e4ce60d4"',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
    },
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json)
    }).catch((err) => console.log(err))

  }).catch((err) => console.log(err))
}

exports.userFollowers = (username, count) => {
  fetch('https://i.instagram.com/api/v1/users/web_profile_info/?username=' + username, {
  method: 'GET',
  headers: {
    'Content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
  },
})
  .then((response) => response.json())
  .then((json) => {
    const usernameId = json.data.user.id;

    //returning "count" number of followers accounts
    fetch('  https://www.instagram.com/api/v1/friendships/' + usernameId + '/followers/?count=' + count + '&search_surface=follow_list_page', {
    method: 'GET',
    headers: {
        'Content-type': 'application/json',
        'cookie': 'mid=ZKb90AAEAAHeJHFiThh3YHbtXxFj; ig_did=E1C82320-9298-44E8-AC11-0B73FD6F2A4B; csrftoken=8jpjVzXIehbiWFoXmJWtWVDV1KqA4gf4; ds_user_id=60150778235; sessionid=60150778235%3A1mkfoRdfeVMIfV%3A27%3AAYfcGNpKvqJ0XqWyTKU1doUREaFBvdK2nWSu-qKrEA; dpr=2.200000047683716; rur="CLN\x2c5460150778235\x2c541720202385:01f7588c3129eb9765ff944a46f68d000cc6030e5acb76cbc4f81d0fad5933a3e4ce60d4"',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
    },
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json)
    }).catch((err) => console.log(err))

  }).catch((err) => console.log(err))
}

exports.userFeedText = (username, count) => {
  fetch('https://www.instagram.com/api/v1/feed/user/' + username + '/username/?count=' + count, {
  method: 'GET',
  headers: {
    'Content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
  },
})
  .then((response) => response.json())
  .then((json) => {
    const feedTexts = [];
    json.items.forEach(element => {
      feedTexts.push(element.caption.text)
    });
    console.log(feedTexts)

  }).catch((err) => console.log(err))
}