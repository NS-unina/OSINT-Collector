"""OSINT-Collector tool launcher"""
import typer

app = typer.Typer()


def main(name: str):
    """Default tool launcher"""
    print(f"Launch {name}")


if __name__ == "__main__":
    app()
