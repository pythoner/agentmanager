import base
import re
import json
from agentmanager.service import agent as agent_service
from agentmanager.common import log
from agentmanager.util import conf
import requests

worker_host = conf.get_conf('worker', 'api_host', default='10.121.8.85')
worker_port = conf.get_conf('worker', 'port', default='8080')
LOG = log.logger(__name__)


class AgentHandler(base.BaseHandler):
    def abstract_get(self):
        response = None
        project_id = self.get_project_id()
        if re.match(r'^/agents$', self.request.path):
            response = self.get_agents(project_id)
        elif re.match(r'^/agents/(-?[0-9a-zA-Z]+)$', self.request.path):
            ids = self.request.path.split('/')
            response = self.get_agent_by_id(ids[2], project_id)
        self.write(response)

    def get_agent_by_id(self, agent_id, project_id, is_admin=False):
        # rbac.enforce("show_agent", self.request)
        response = agent_service.get_agent_by_id(agent_id, project_id, is_admin)
        return json.dumps(response)

    def get_agents(self, project_id, is_admin=False):
        """
        paging add argument pageno, pagesize
        eg: http://127.0.0.1:8080/agents?pageno=1&pagesize=20
        default page size is 20
        :return:
        """
        # rbac.enforce("list_agents", self.request)
        if is_admin:
            response = agent_service.get_agents(self.query)
        else:
            response = agent_service.get_agents(self.query, project_id)
        return json.dumps(response)

    def create_worker(self, agent_name, token, timezone, url, org_name, interval):
        data = {}
        project_name = self.get_project_name()
        data["config_params"] = {"CP_ORG_KEY": token, "CP_ORG_TZ": timezone, "CP_MGMT_URL": url,
                                 "CP_ORG_NAME": org_name, "REPORT_INTERVAL": interval, "OI_TENANT": project_name}
        data["collector_name"] = agent_name
        url = "http://{host}:{port}/cp_collector/".format(host=worker_host, port=worker_port)
        response = requests.post(url, json=data)
        LOG.info(response.text)
        data = json.loads(response.text)
        return data.get("result")

    def stop_worker(self, worker_name):
        url = "http://{host}:{port}/cp_collector/{name}".format(host=worker_host, port=worker_port, name=worker_name)
        response = requests.delete(url)
        LOG.info(response.text)
        return json.loads(response.text)

    def abstract_post(self):
        # rbac.enforce("create_agent", self.request)
        config_params = self.json_body.get("meta")
        token, timezone, url, org_name, interval = \
            config_params.get("access_token"), config_params.get("time_zone"), config_params.get("url"), \
            config_params.get("orgnization_name"), config_params.get("report_interval"),
        try:
            timezone = int(timezone)
            if timezone < -12 or timezone > 12:
                raise
        except Exception as e:
            return self.write(self.packaging_result(False, "time zone should be integer between -12 and 12"))
        try:
            interval = int(interval)
            if interval <= 0:
                raise
        except Exception as e:
            return self.write(self.packaging_result(False, "report interval should be integer and bigger than 0"))
        agent_name = self.json_body.get("name")
        result = self.create_worker(agent_name, token, timezone, url, org_name, interval)
        if not result:
            response = self.packaging_result(False, "create worker failed")
            return self.write(response)
        project_id = self.get_project_id()
        project_name = self.get_project_name()
        self.json_body.update({"project_id": project_id, "project_name": project_name})
        agent_service.add_agents(**self.json_body)
        response = self.packaging_result(True)
        self.write(response)

    def check_agent_id(self):
        matched = re.match(r'^/agents/(-?[0-9a-zA-Z]+)$', self.request.path)
        if not matched:
            return False, 0
        ids = self.request.path.split('/')
        return True, ids[2]

    def abstract_put(self):
        # rbac.enforce("update_agent", self.request)
        result, agent_id = self.check_agent_id()
        if not result:
            response = self.packaging_result(False, "need agent id")
            self.write(response)
        project_id = self.get_project_id()
        result = agent_service.get_agent_by_id(agent_id, project_id)
        if not result:
            response = self.packaging_result(False, "There is not agent with id %s" % agent_id)
            return self.write(response)
        agent_service.update_agent_by_id(agent_id, **self.json_body)
        return self.write(self.packaging_result(True))

    def abstract_delete(self):
        # rbac.enforce("delete_agent", self.request)
        result, agent_id = self.check_agent_id()
        if not result:
            response = self.packaging_result(False, "need agent id")
            return self.write(response)
        project_id = self.get_project_id()
        result = agent_service.get_agent_by_id(agent_id, project_id)
        if not result:
            response = self.packaging_result(False, "There is not agent with id %s" % agent_id)
            return self.write(response)
        response = self.stop_worker(result.get("name"))
        if not response.get("result"):
            resp = self.packaging_result(False, response.get("msg", ""))
            return self.write(resp)
        agent_service.update_agent_by_id(agent_id, deleted=1)
        return self.write(self.packaging_result(True))

    def packaging_result(self, result, description=""):
        return json.dumps({"result": result, "description": description})

    def get_project_id(self):
        return self.request.headers.get("X-Project-Id", self.request.headers.get("X-Tenant-Id", ""))

    def get_project_name(self):
        return self.request.headers.get("X-Project-Name", self.request.headers.get("X-Tenant-Name", ""))





