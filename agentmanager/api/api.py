import sys

from agentmanager.api import app
from agentmanager.common import log

from oslo_config import cfg

log.InitLog('agentmanager-api.log')


def prepare_service(argv=None):
    if argv is None:
        argv = sys.argv
    cfg.CONF(argv[1:], project='agentmanager')


def agentmanager_api():
    prepare_service([])
    app.server('agentmanager_api', '/etc/agentmanager/api-paste.ini')


if __name__ == "__main__":
    agentmanager_api()
