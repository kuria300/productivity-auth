import os

class Config:
    DEBUG=True
    """ sensitive database information"""
    SQLALCHEMY_DATABASE_URI= 'sqlite:///app.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


