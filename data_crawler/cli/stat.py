
import click
from data_crawler import stat

@click.command()
@click.option('--production', is_flag=True)
def main(production):
    """Console script for """

    click.echo("Running...  stat")
    stat.main(production)


if __name__ == "__main__":
    main()
