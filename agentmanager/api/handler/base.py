import tornado.web

import traceback

from agentmanager.common import exception
from agentmanager.common import log
from agentmanager.common import models
from agentmanager.util import conf

LOG = log.logger(__name__)
ADMIN_USER = conf.get_conf('administrator', 'user')
ADMIN_PASSWORD = conf.get_conf('administrator', 'password')

NUMBER_QUERY_TYPE = ['number', 'integer', 'float']


class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.set_header("Content-Type", "application/json")
        self.query = self.__generate_query(self.request.arguments)
        LOG.info('Request path is %s ' % self.request.path)
        if self.request.body:
            self.json_body = tornado.escape.json_decode(self.request.body)
            LOG.info('Request body is %s ' % self.request.body)

    def get(self):
        try:
            self.abstract_get()
        except exception.AuthError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(401)
        except exception.ForbiddenError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.NotFoundError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(404)
        except Exception as e:
            LOG.error('Exception type is %s, message is %s'
                      % (e.__class__.__name__, e))
            LOG.error(traceback.format_exc())
            self.write('Please contract the admin')
            self.set_status(500)

    def abstract_get(self):
        pass

    def post(self):
        try:
            self.abstract_post()
            self.set_status(201)
        except exception.ConflictError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(409)
        except exception.InvalidInputError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(400)
        except exception.ForbiddenError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.AuthError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(401)
        except exception.SaveError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.BadRequestError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(400)
        except Exception as e:
            LOG.error('Exception type is %s, message is %s'
                      % (e.__class__.__name__, e))
            LOG.error(traceback.format_exc())
            self.write('Please contract the admin')
            self.set_status(500)

    def abstract_post(self):
        pass

    def put(self):
        try:
            self.abstract_put()
        except exception.InvalidInputError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(400)
        except exception.AuthError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(401)
        except exception.UpdateError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.ForbiddenError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.NotFoundError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(404)
        except exception.ConflictError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(409)
        except exception.BadRequestError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(400)
        except Exception as e:
            LOG.error('Exception type is %s, message is %s'
                      % (e.__class__.__name__, e))
            LOG.error(traceback.format_exc())
            self.write('Please contract the admin')
            self.set_status(500)

    def abstract_put(self):
        pass

    def delete(self):
        try:
            self.abstract_delete()
            self.set_status(201)
        except exception.AuthError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(401)
        except exception.DeleteError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.ForbiddenError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(403)
        except exception.NotFoundError as e:
            self.write(e.msg)
            LOG.error(e.msg)
            self.set_status(404)
        except Exception as e:
            LOG.error('Exception type is %s, message is %s'
                      % (e.__class__.__name__, e))
            LOG.error(traceback.format_exc())
            self.write('Please contract the admin')
            self.set_status(500)

    def abstract_delete(self):
        pass

    def __generate_query(self, arguments):
        LOG.info(arguments)
        if len(arguments) == 0:
            query = models.Query()
            query.set_query({}, 1, 10, "updated", -1)
            return query
        try:
            # if 'q.field' in arguments:
            #     fields = arguments['q.field']
            #     values = arguments['q.value']
            #     op = arguments['q.op']
            #     # q.type is optional
            #     if 'q.type' in arguments:
            #         qtype = arguments['q.type']
            #     else:
            #         qtype = None
            # else:
            #     fields = []
            # get all result in one page and positive sequence returned
            # in order by id as default
            pageno = 1
            pagesize = 10
            order_by = 'updated'
            sort = -1
            if 'pageno' in arguments:
                pageno = int(arguments.pop('pageno')[0])
            if 'pagesize' in arguments:
                pagesize = int(arguments.pop('pagesize')[0])
        except Exception as e:
            LOG.error('Exception type is %s, message is %s'
                      % (e.__class__.__name__, e))
            LOG.error(traceback.format_exc())
            self.set_status(500)
            raise
        fields = []
        querys = {}
        for k, v in arguments.items():
            querys.setdefault(k, v[0])
        # for i in range(0, len(fields)):
        #     querys += fields[i] + self.__get_op(op[i])
        #     # qtype is optional
        #     if qtype and qtype[i] in NUMBER_QUERY_TYPE:
        #         querys += values[i]
        #     else:
        #         querys += "'" + values[i] + "'"
        #     if i != len(fields) - 1:
        #         querys += ' and '
        query = models.Query()
        query.set_query(querys, pageno, pagesize, order_by, sort)
        return query

    def __get_op(self, op):
        if 'eq' == op:
            return '='
        elif 'gt' == op:
            return '>'
        elif 'lt' == op:
            return '<'
        elif 'ge' == op:
            return '>='
        elif 'le' == op:
            return '<='
        elif 'nq' == op:
            return '!='
        else:
            return None
