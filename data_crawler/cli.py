
import click
from data_crawler.main import data_crawler

@click.command()
@click.option('--production', is_flag=True)
def main(production):
    """Console script for """

    click.echo("Running...  data crawler of Technukrom")
    data_crawler(production)

if __name__ == "__main__":
    main()
