# Requirements
In order to use the following launcher, you should have Docker and Docker Compose installed.

# Startup
It is possible to run the whole architecture by starting the docker-compose with:
```
docker-compose up -d
```

Then, a web server will listen on port 5000.

# Web Server

To use the architecture, it is possible to interact with the web server by listening on port 5000 with HTTP requests (at the moment, no SSL has been provided).

The following endpoints have been provided:

## Available Tools Retrieval 

This endpoint provides, as a response, a list of supported tools.

Endpoint: ```/tools```

Usage example:
```
curl --location 'http://localhost:5000/tools'
```

Response example:
```
[
    "snscrape-telegram",
    "the-harvester",
    "instaloader",
    "telegram-tracker",
    "blackbird"
]
```

## Tool Details

As a response, this endpoint provides all the details about the provided tool.

Endpoint: ```\tools\:tool_name``` 

Usage example:
```
curl --location 'http://localhost:5000/tools/telegram-tracker'
```

Response Example:
```
{
    "description": "Download messages from the given telegram channel.",
    "entrypoints": [
        {
            "command": "python3 main.py --telegram-channel ${CHANNEL} -o /output",
            "description": "Download the last message in the provided channel",
            "inputs": [
                "CHANNEL"
            ],
            "key": "download-group-messages"
        }
    ],
    "inputs": [
        {
            "description": "The telegram channel where to extract the last message",
            "format_type": "string",
            "key": "CHANNEL"
        }
    ],
    "name": "telegram-tracker"
}
```

## Tool Execution

This endpoint allows the tool execution and output data generation.

Endpoint: ```\launch```

Usage example:
```
curl --location 'http://localhost:5000/launch' \
     --header 'Content-Type: application/json' \
     --data '{
        "image" : "telegram-tracker",
        "entrypoint": "download-group-messages",
        "inputs": ["osintcollector_group"]
     }'
```

Response Example:
```
OK
```

# Tools Management

Each tool defined into the ```/tools/<tool-name>``` folder should have a Dockerfile named ```Dockerfile``` containing the necessary steps to build the docker image, a ```<tool-name>.yml``` file containing the entrypoint and the expected inputs and a ```<tool-name>.conf``` containing the Logstash pipeline to filter the data.

Structure example:
```
tools
├── <tool-name-1>
│    ├── Dockerfile
│    ├── <tool-name-1>.yml
│    └── <tool-name-1>.conf
│
├── <tool-name-2>
│    ├── Dockerfile
│    ├── <tool-name-2>.yml
│    └── <tool-name-2>.conf
│
├── ...
│
└── <tool-name-N>
     ├── Dockerfile
     ├── <tool-name-N>.yml
     └── <tool-name-N>.conf
```

## YAML File

The ```<tool-name>.yml``` is responsible for defining the tool's behaviour; the file structure looks like:
```
<tool-name>:
    description: <tool-description>
    entrypoints: 
        - key: <entrypoint-unique-key>
          name: <human-readable-entrypoint-name>
          description: <entrypoint-description>
          inputs:
            - <entrypoint-required-input-key-1>
            - ...
          command: <entrypoint-execution-command>
        - ...

    inputs:
        - key: <input-unique-key-uppercased>
          description: <input-description>
          type: <input-type>
        - ...
```

Example of a tool named "exampletool" that defines three inputs (InputA, InputB, InputC) and two entrypoint:
- entrypoint1: execute ./execute-something and requires InputA with flag -a and InputC with flag -c
- entrypoint2: execute ./execute-something-else requires InputB with flag -b

```
exampletool:
    description: An example tool to understand the yml structure
    entrypoints: 
        - key: entrypoint-1
          name: Entrypoint 1
          description: The first entrypoint of exampletool
          inputs:
            - INPUTA
            - INPUTC
          command: ./execute-something -a ${INPUTA} -c ${INPUTC}

        - key: entrypoint-2
          name: Entrypoint 2
          description: The second entrypoint of exampletool
          inputs:
            - INPUTB
          command: ./execute-something-else -b ${INPUTB}

    inputs:
        - key: INPUTA
          description: Define the A input
          type: string

        - key: INPUTB
          description: Define the B input
          type: integer

        - key: INPUTC
          description: Define the C input
          type: double
```

Notice that in the entrypoint command, you can use the defined entrypoint inputs by using a bash-style interpolation of environment variables ```${<input-key>}```. 

Moreover, the launcher expects that the tool will provide output in the /output container folder mapped on the host in the ```output/<tool-name>``` folder.

## CONF File

The ```<tool-name>.conf``` is responsible for handling the filter process; the file structure looks like:
```
input {
  file {
    ...
    path => "/output/<output-file>"
 }
}


filter {
  ...
}

output {
  file {
    codec => json
    path => "/output/<tool-name>-logstash.json"
  }
}
```