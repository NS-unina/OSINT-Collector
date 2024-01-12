// types.ts
export interface Capability {
    id: number;
    name: string;
  }
  
export interface ServerResponse {
    capability_parameters: string[];
}

export interface RequiredInput {
    input: {
        label: string;
        name: string;
    }[];
    tool: {
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