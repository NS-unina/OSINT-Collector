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
    flag: boolean;
    posts: {
        id: string;
        url: string;
        shortcode: string;
        text: string;
        timestamp: number;
        likes: number;
        comments: number;
        taggedAccounts: string[];
        location: {
            name: string;
        }
        processed: boolean;
        categories: {
            uri: string;
            name: string;
            alsoKnownAs: string;
        } [];
    } [];
}

export interface InstagramAccount {
    full_name: string;
    followers: number;
    bio_links: string[];
    biography: string;
    id: string;
    follow: number;
    profile_pic_url: string;
    username: string;
    flag: boolean;
}

export interface TelegramChannel {
    name: string;
    flag: boolean;
}

export interface InstagramPost {
    id: string;
    url: string;
    shortcode: string;
    text: string;
    timestamp: number;
    likes: number;
    comments: number;
    taggedAccounts: string[];
    location: {
        name: string;
    }
    processed: boolean;
    categories: {
        uri: string;
        name: string;
        alsoKnownAs: string;
    } [];
}

export interface Category {
    uri: string;
    name: string;
    alsoKnownAs: string;
}

export interface TelegramPost { 
    url: string;
    date: string;
    text: string;
    processed: boolean;
    categories: {
        uri: string;
        name: string;
        alsoKnownAs: string;
    } [];
}

export interface Category {
    uri: string;
    name: string;
    alsoKnownAs: string;
}

export interface Location {
    id: string;
    name: string;
}

export interface TelegramUser {
    id: string;
    first_name: string;
    last_name: string;
    username: string;
    phone: string;
    bot: boolean;
    verified: boolean;
    premium: boolean;
    flag: boolean;
    messages?: TelegramMessage[];
}

export interface TelegramMessage {
    id: string;
    messageType: string;
    peer_id: string;
    from_id: string;
    date: string;
    edit_date: string;
    message: string;
    pinned: boolean;
    reply_to_id: string;
    processed: boolean;
    categories?: Category[];
    repliedMessage?: TelegramMessage;
}

export interface TelegramGroup {
    id: string;
    about: string;
    title: string;
    username: string;
    date: string;
    participants_count: string;
    flag: boolean;
    messages?: TelegramMessage[];
}