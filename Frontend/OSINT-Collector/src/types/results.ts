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
    pippo: string;
    posts: string[];
}