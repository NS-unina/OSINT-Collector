# Requirements
In order to use the following launcher you should have Docker and Docker Compose installed.

# Usage
It is possible to run the launcher from Command Line Interface with the following:
```
./main.py <tool-name> -e <entrypoint> -i <inputs-space-separated>
```

# Tools Management

Each tool defined into the ```/tools/<tool-name>``` folder should have a Dockerfile named ```Dockerfile``` containing the necessary steps to build the docker image and a ```<tool-name>.yml``` file containing the entrypoint and the expected inputs.

Structure example:
```
tools
└── <tool-name>
    ├── Dockerfile
    └── <tool-name>.yml
```

The ```<tool-name>.yml``` is responsible for handling all the tool lifecycle, from it's inputs to it's execution; a complete structure will consist in:
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

Notice that in the entrypoint command you can use the defined entrypoint inputs by using a bash-style interpolation of environment variables ```${<input-key>}```. 

Moreover, the launcher expect that an output will be provided by the tool in the /output container folder mapped on the host in the ```output/<tool-name>``` folder.