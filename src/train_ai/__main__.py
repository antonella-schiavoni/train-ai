"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Train Ai."""


if __name__ == "__main__":
    main(prog_name="train-ai")  # pragma: no cover
