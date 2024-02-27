// types.ts
export interface Platform {
    id: number;
    name: string;
}

export interface Capability {
    id: number;
    name: string;
    description: string;
}

export interface Launch {
    id: number;
    image: string;
    entrypoint: string;
    completed: boolean;
    timestamp: number;
    inputs: string[];
}
  
export interface ServerResponse {
    capability_parameters: string[];
}

export interface RequiredInput {
    inputs: {
        id: string;
        label: string;
        name: string;
        uri: string;
    }[];
    capability: {
        id: string;
        name: string;
    }
    tool: {
        id: string;
        name: string;
        platform: string;
    };
}

export interface GetToolsResponse {
    tools: Tool[];
}

export interface Tool {
    id: number;
    name: string;
}

export interface RequiredToolInputs {
    inputs: {
        label: string;
        value: string;
    }[];
    capability: {
        name: string;
    }
    tool: {
        name: string;
    };
}
  
export interface RunToolForm {
    timestamp: string;
    image: string;
    entrypoint: string;
    inputs: string[];
}

export interface SearchResult {
    cacheUrl: string;
    clicktrackUrl: string;
    content: string;
    contentNoFormatting: string;
    title: string;
    titleNoFormatting: string;
    formattedUrl: string;
    unescapedUrl: string;
    url: string;
    visibleUrl: string;
    richSnippet: {
      cseImage: {
        src: string;
      };
      metatags: {
        twitterTitle: string;
        twitterSite: string;
        handheldfriendly: string;
        ogTitle: string;
        ogDescription: string;
        twitterDescription: string;
    }
    };
    breadcrumbUrl: {
        "host": string;
        "crumbs": [
            string
        ]
    }
  }

export interface GoogleSearchResponse {
    error: {
        code: number;
        message: string;
    };
    cursor: {
      currentPageIndex: number;
      estimatedResultCount: string;
      moreResultsUrl: string;
      resultCount: string;
      searchResultTime: string;
      pages: {
        label: number;
        start: string;
      }[];
    };
    context: {
      title: string;
      total_results: string;
    };
    results: SearchResult[];
    findMoreOnGoogle: {
      url: string;
    };
  }