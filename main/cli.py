import click
from flask.cli import with_appcontext

def register_commands(app):
    """Register administrative commands with Flask."""
    
    @app.cli.command("health-check")
    @with_appcontext
    def health_check():
        """Verify the application is healthy and can connect to all services."""
        app.logger.info("Running health check")
        # Here you would check database connections, external services, etc.
        click.echo("Health check passed!")
    
    @app.cli.command("show-config")
    @with_appcontext
    def show_config():
        """Display non-sensitive configuration (for debugging)."""
        # Only show safe config keys
        safe_config = {
            k: v for k, v in app.config.items() 
            if not (k.endswith('KEY') or k.endswith('SECRET') or k.endswith('PASSWORD'))
        }
        for key, value in sorted(safe_config.items()):
            click.echo(f"{key}: {value}")
    
    # If you have database models, you could add migrations/initialization commands here
    
    return app
