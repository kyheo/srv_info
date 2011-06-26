import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('In the future, the information will be listed'
                ' in here.')


class Notification(webapp.RequestHandler):
    def get(self, client_id=None):
        logging.debug('Notification.get called with client_id: %s from ip: %s' % 
                (client_id, self.request.remote_addr))
        self.error(405)
        self.response.headers.add_header("Error-Message", 
                'Use HTTP POST method to send reports.')
 

    def post(self, client_id):
        logging.debug('Notification.post with client_id: %s from ip: %s' % 
                (client_id, self.request.remote_addr))


routes = [
        ('/notify/([a-zA-Z0-9]+)', Notification), 
        ('/', MainPage), 
        ]


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(routes, debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
