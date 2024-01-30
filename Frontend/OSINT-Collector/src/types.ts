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
    image: string;
    entrypoint: string;
    inputs: string[];
}