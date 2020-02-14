from agentmanager.db import agent as db_agent
import time
from agentmanager.common import log

LOG = log.logger(__name__)


def get_agent_by_id(agent_id, project_id):
    result = db_agent.get_agent_by_id(agent_id, project_id)
    if result:
        result["_id"] = str(result["_id"])
        result.pop("deleted")
    return result


def add_agents(**kwargs):
    kwargs["deleted"] = 0
    kwargs["created"] = kwargs["updated"] = int(time.time())
    kwargs["managed"] = True
    return db_agent.create_agent(kwargs)


def update_agent_by_id(agent_id, **kwargs):
    kwargs["updated"] = int(time.time())
    return db_agent.update_agent_by_id(agent_id, kwargs)


def get_agents(query, project_id="", exclude_deleted=True, **kwargs):
    kwargs.update({"managed": True})
    if project_id:
        kwargs.update({"project_id": project_id})
    if exclude_deleted:
        kwargs.update({"deleted": 0})
    result = db_agent.get_agents(query, **kwargs)
    response = []
    for item in result:
        item["_id"] = str(item["_id"])
        item.pop("deleted")
        response.append(item)
    return response


