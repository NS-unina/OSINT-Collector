
# Notes

Each tool defined into the /tools folder should have a folder named with the name of the tool and that folder should contains at least the following files:
- Dockerfile: containing the necessary steps to build the docker image to use the defined tool

Structure example:
```
tools
└── <tool-name>
    └── Dockerfile
```