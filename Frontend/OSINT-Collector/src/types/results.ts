export interface blackbird {
    username: string;
    sites: {
        id: number;
        site: string;
        status: string;
        url: string;
    } [];
}

export interface snscrape {
    name: string;
    flag: boolean;
    posts : {
        url: string;
        date: string;
        text: string;
        processed: boolean;
        categories: {
            uri: string;
            name: string;
            alsoKnownAs: string;
        } [];
    } [];
}

export interface instaloader {
    full_name: string;
    followers: number;
    bio_links: string[];
    biography: string;
    id: string;
    follow: number;
    profile_pic_url: string;
    username: string;
    posts: {
        id: string;
        url: string;
        shortcode: string;
        text: string;
        timestamp: number;
        likes: number;
        comments: number;
        taggedAccounts: string[];
        processed: boolean;
        categories: {
            uri: string;
            name: string;
            alsoKnownAs: string;
        } [];
    } [];
}

export interface TelegramChannel {
    name: string;
    flag: boolean;
}