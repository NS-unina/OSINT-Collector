import argparse

import uvicorn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        default="127.0.0.1",
        help="IP address to listen on default is 127.0.0.1",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=5000,
        help="Port to bind the web server to, default is 5000",
        type=int,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="info",
        help="Set logging level, default is info but [critical|error|warning|info|debug|trace] can be set",
    )
    parser.add_argument(
        "-r",
        "--reload",
        default=False,
        help="Enable automatic reload used during development of the api",
        action="store_true",
    )

    args: argparse.Namespace = parser.parse_args()
    uvicorn.run(
        "theHarvester.lib.api.api:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
