from ..core.term import Terminal
from ..core.viewerData import Viewer
import click

@click.command(help="Open a terminal created previously.")
@click.argument('name')
@click.option('--id', default=0, help='id of terminal.')
def open(name, id):
  terminal = Terminal(name=name, id=id)
  viewer = Viewer(terminal)
  viewer.show()

@click.command(help="Delete a terminal created previously.")
@click.argument('name')
@click.option('--id', default=0, help='id of terminal.')
def delete(name, id):
  print ("Abriendo terminal", name, id)

@click.command(help="Create a new terminal.")
@click.argument('name')
@click.option('--id', default=0, help='id of terminal.')
def create(name, id):
  print ("Abriendo terminal", name, id)

@click.command(help="List all terminals.")
@click.argument('name')
@click.option('--id', default=0, help='id of terminal.')
def list(name, id):
  print ("Abriendo terminal", name, id)

@click.group
def cli():
    pass

cli.add_command(open)
cli.add_command(delete)
cli.add_command(create)
cli.add_command(list)

def main():
    cli()