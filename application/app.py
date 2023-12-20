"""Module for application configuration"""
from fastapi import FastAPI

from . import init_app


def create_app():
    """Application configuration

    Returns:
        Object: Instance of application
    """
    app = FastAPI()

    init_app(app)

    return app
