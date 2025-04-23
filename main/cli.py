import click
from flask import current_app
from . import db

def register_cli(app):
    @app.cli.command("db-init")
    def db_init():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
            click.echo("Database tables created.")
