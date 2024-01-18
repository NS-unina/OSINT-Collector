// types.ts
export interface Platform {
    id: number;
    name: string;
}

export interface Capability {
    id: number;
    name: string;
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