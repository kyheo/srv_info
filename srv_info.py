import logging
import json
import datetime

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class Event(db.Model):
    client   = db.StringProperty()
    date     = db.DateTimeProperty(auto_now_add=True)
    category = db.StringProperty()
    ip       = db.StringProperty()
    data     = db.TextProperty()

    def __str__(self):
        return "[%s] %s (%s): %s - %s" % (self.date, self.client, self.ip,
                self.category, self.data)

    @property
    def decoded_data(self):
        return json.loads(self.data)


class MainPage(webapp.RequestHandler):
    def get(self):
        
        events = Event.all()
        clients = set([event.client for event in events])
        categories = set([event.category for event in events])

        if self.request.get('client'):
            events.filter('client = ', self.request.get('client'))
        if self.request.get('category'):
            events.filter('category = ', self.request.get('category'))
       
        data = {'events': events.order('-date').fetch(10),
                'clients': clients,
                'categories': categories,
                'now': datetime.datetime.now()}
        self.response.out.write(template.render('templates/home.tpl', data))

    def post(self):
        return self.get()


class Notification(webapp.RequestHandler):

    def post(self, client, category='default'):
        """ Stores the given event in the storage
        
        Example::

            $ wget -O - --post-data='data={"eth0":null, "lo": "127.0.0.1", \
                "wlan0":"192.168.1.104"}' http://localhost:8080/notify/nibbler/ip

            $ wget -O - --post-data='data={"uptime": "19:40:11 up 6 min,  4 \
                users,  load average: 0.02, 0.27, 0.19"}' \
                http://localhost:8080/notify/nibbler/uptime
        """
        logging.debug('Notification.post with client: %s from ip: %s' % 
                (client, self.request.remote_addr))
        if not client:
            self.error(400)
            self.response.headers.add_header('Error-Message',
                    'Missing client id.')
        else:
            event = Event(client=client, category=category,
                    ip=self.request.remote_addr)
            if self.request.get('data'):
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
