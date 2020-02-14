import agentmanager.db.factory as db_factory
from bson import objectid
from agentmanager.common import log
LOG = log.logger(__name__)


def _get_db(db):
    connection = db_factory.get_connection()
    return connection.get_database(db)


def get_agent_by_id(agent_id, project_id):
    db = _get_db("oi")
    result = db.agents.find_one({"_id": objectid.ObjectId(agent_id), "deleted": 0, "project_id": project_id})
    return result


def update_agent_by_id(agent_id, body):
    db = _get_db("oi")
    result = db.agents.update_one({"_id": objectid.ObjectId(agent_id)}, {"$set": body})
    return result


def create_agent(body):
    db = _get_db("oi")
    result = db.agents.insert_one(body)
    return result


def get_agents(query, **kwargs):
    db = _get_db("oi")
    limit = query.pagesize
    offset = query.get_start()
    order_by = query.order_by
    sort = query.sort
    kwargs.update(query.query)
    result = db.agents.find(kwargs).sort([(order_by, sort)]).limit(limit).skip(offset)
    return result
