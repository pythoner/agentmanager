# from api_sqlalchemy import SQLAlchemyConnection
from pymongo import MongoClient

from agentmanager.util import conf

CONNECTION = None


def get_connection():
    global CONNECTION
    if not CONNECTION:
        connection = conf.get_conf('database', 'connection')
        if connection.startswith('mongodb'):
            CONNECTION = MongoClient(connection)
    return CONNECTION
