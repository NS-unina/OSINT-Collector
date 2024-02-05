export interface blackbird {
    username: string;
    sites: {
        id: number;
        site: string;
        status: string;
        url: string;
    } [];
}

export interface instaloader {
    pippo: string;
    posts: string[];
}