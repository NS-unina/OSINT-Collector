# Requirements
In order to use the following launcher you should have Docker and Docker Compose installed.

# Usage
It is possible to run the launcher from Command Line Interface with the following:
```
./launcher.py <tool-name> -i <inputs-space-separated>
```

# Tools Management

Each tool defined into the /tools/<tool-name> folder should have a Dockerfile named using the following convention: "<tool-name>.Dockerfile" containing the necessary steps to build the docker image and a "<tool-name>.yml" file containing the entrypoint and the expected inputs.

Structure example:
```
tools
└── <tool-name>
    ├── <tool-name>.Dockerfile
    └── <tool-name>.yml
```

After that, just add a service into the docker-compose.yml file to start the tool; a common structure is provided; it make the following assuntions:
- The Dockerfile is in the ./tools/<tool-name>/<tool-name>.Dockerfile format
- The image will be named with the tool name
- The container will be named with the tool name
- The services output should be placed in the /output container folder (mapped in the output/<tool-name> host folder)
- The entrypoint will be provided in the <tool-name>.yml file

In the <tool-name>.yml file the entrypoint should contains a reference to specific input, the convention used is $<input-key>; for example if a tool called "exampletool" defines an entrypoint that requires the input DOMAIN with flag -d, the file should be in the format of:
```
exampletool:
    entrypoint: ./path/to/tool -d $DOMAIN
    inputs:
        - DOMAIN: A description of what this input is
```