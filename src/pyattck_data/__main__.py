"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Pyattck Data."""


if __name__ == "__main__":
    main(prog_name="pyattck-data")  # pragma: no cover
