import os
import traceback

from paste import deploy
import tornado.ioloop
import tornado.web
import tornado.wsgi
from werkzeug import serving

from agentmanager.api.handler import agent
from agentmanager.api.handler import nopage
from agentmanager.common import log
from agentmanager.util import conf

LOG = log.logger(__name__)

API_SERVER_PROCESS = conf.get_conf_int('agentmanager', 'api_server_process',
                                       default=10)
# agentmanager_API_PORT = conf.get_conf_int('agentmanager', 'api_port', default=7207)
agentmanager_API_PORT = conf.get_conf_int('agentmanager', 'api_port', default=8081)
agentmanager_API_HOST = conf.get_conf('agentmanager', 'api_host', default='0.0.0.0')


class API(object):

    def __init__(self, app):
        self.application = app

    def __call__(self, environ, start_response):
        return self.application.__call__(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return None


class AgentManagerAPI(API):

    def __init__(self):
        app = tornado.wsgi.WSGIApplication([
            # (r"/account.*", account.AccountHandler),
            (r"/agents.*", agent.AgentHandler),
            (r".*", nopage.NoPageHandler),
        ])
        super(AgentManagerAPI, self).__init__(app)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return AgentManagerAPI()


def server(app_name, conf_file):
    app = load_paste_app(app_name, conf_file)
    LOG.info('---------------------Start agentmanager API---------------------')
    serving.run_simple(agentmanager_API_HOST, agentmanager_API_PORT, app,
                       processes=API_SERVER_PROCESS)


def load_paste_app(app_name, conf_file):
    LOG.debug('Loading %s from %s' % (app_name, conf_file))

    try:
        app = deploy.loadapp("config:%s" %
                             os.path.abspath(conf_file), name=app_name)
        return app
    except (LookupError, ImportError) as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        raise RuntimeError(str(e))
