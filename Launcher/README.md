# Requirements
In order to use the following launcher you should have Docker and Docker Compose installed.

# Usage
It is possible to run the launcher from Command Line Interface with the following:
```
./launcher.py <tool-name> -i <input-string>
```

# Tools Management

Each tool defined into the /tools folder should have a folder named with the name of the tool and should contains a Dockerfile containing the necessary steps to build the docker image to use the defined tool.

Structure example:
```
tools
└── <tool-name>
    └── Dockerfile
```

After that, just add a service into the docker-compose.yml file to start the tool; a common structure is provided; it make the following assuntions:
- The Dockerfile is in the ./tools/<tool-name> folder
- The image will be named with the tool name
- The container will be named with the tool name
- The services output should be placed in the /output container folder (mapped in the output/<tool-name> host folder)
