import logging
import json
import datetime

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app


class Event(db.Model):
    client = db.StringProperty()
    date   = db.DateTimeProperty(auto_now_add=True)
    type_  = db.StringProperty()
    ip     = db.StringProperty()
    data   = db.TextProperty()

    def __str__(self):
        return "Event: %s - %s - %s - %s" % (self.client, self.date.isoformat(),
                self.type_, self.data)

    @property
    def decoded_data(self):
        return json.loads(self.data)


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><head><title>SRV_INFO - Event log'
                '</title></head><body>'
                '<b>In the future, the information will be listed in here.</b>'
                '<h1>Event log</h1>')
        for event in Event.all().order('-date'):
            self.response.out.write(event)
            self.response.out.write('<hr>')
        self.response.out.write('<i>Page generated on %s</i>' %
                (datetime.datetime.now(),))
        self.response.out.write('</body></html>')


class Notification(webapp.RequestHandler):
    def get(self, client=None):
        logging.debug('Notification.get called with client: %s from ip: %s' % 
                (client, self.request.remote_addr))
        self.error(405)
        self.response.headers.add_header("Error-Message", 
                'Use HTTP POST method to send reports.')
 

    def post(self, client, type_='default'):
        logging.debug('Notification.post with client: %s from ip: %s' % 
                (client, self.request.remote_addr))
        if not client:
            self.error(400)
            self.response.headers.add_header('Error-Message',
                    'Missing client id.')
        else:
            event = Event(client=client, type_=type_,
                     ip=self.request.remote_addr)
            if self.request.get('data'):
                #TODO Validate valid json, valid structure
                event.data = self.request.get('data')
            event.put()


routes = [
        ('/notify/([a-zA-Z0-9]+)', Notification), 
        ('/notify/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', Notification), 
        ('/', MainPage), 
        ]


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(routes, debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
