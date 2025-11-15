import click
import code

@click.command()
def shell():
    """Opens an interactive Python shell with the app context."""
    try:
        from IPython import start_ipython
        click.echo("Starting IPython shell...")
        start_ipython(argv=[])
    except ImportError:
        click.echo("IPython not found, falling back to standard Python shell.")
        import readline  # optional, for history
        
        vars = globals()
        vars.update(locals())
        
        # You can import and add models/services to the shell context here
        # from apps.users.models import User
        # vars.update({"User": User})
        
        code.InteractiveConsole(vars).interact()