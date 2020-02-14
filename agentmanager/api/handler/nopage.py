import base


class NoPageHandler(base.BaseHandler):
    def get(self):
        response = 'no page found'
        self.write(response)
        self.set_status(404)

    def post(self):
        response = 'no page found'
        self.write(response)
        self.set_status(404)

    def put(self):
        response = 'no page found'
        self.write(response)
        self.set_status(404)
