# -*- coding: utf-8 -*-

"""Top-level package for biodb_team_3."""

__author__ = """colin.birken"""
__email__ = 'colin.birken@gmail.com'
__version__ = '0.1.0'

from .db_manager import Manager
from .interactor import Interactor

def update(connection=None):
    """creates and populates a database"""
    manager = Manager(connection)
    manager.drop_tables()
    manager.create_tables()
    manager.populate_db()

def create_manager(connection=None):
    """creates and returns a Manager object"""
    return Manager()

def create_interactor():
    """Returns an Interactor object"""
    return Interactor()

__all__ = ['update', 'create_manager', 'create_interactor']
