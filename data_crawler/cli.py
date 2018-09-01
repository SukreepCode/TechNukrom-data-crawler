
import click
from data_crawler.main import data_crawler

@click.command()
# @click.option('--unittest-dir', '-d', default="tests", help='Where is tests \
# directory?')
# @click.option('--package-name', '-p', default="", help='Your package name')
# @click.option('--endswith-test', '-s', is_flag=True, help='Naming styles, if \
# enable this flag, pattern is `*_test`')
def main():
    """Console script for """

    click.echo("Running...  data crawler of Technukrom")
    data_crawler()

if __name__ == "__main__":
    main()
