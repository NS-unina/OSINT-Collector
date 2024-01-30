To launch architecture: ```docker-compose up -d```

To launch a tool send a POST request like:
```

curl --location 'http://localhost:5000/launch' \
--header 'Content-Type: application/json' \
--data '{
    "image" : "the-harvester",
    "entrypoint": "search-domain",
    "inputs": ["duckduckgo", "unina.it"]
}'

```