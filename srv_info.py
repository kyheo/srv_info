import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

import parsers

# Add here the users that might see the info
USERS = ['marrese@gmail.com']

# ########################
# Models 
# ########################

class Client(db.Model):
    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def __str__(self):
        return "[%s] %s" % (self.date, self.name)


class Category(db.Model):
    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def __str__(self):
        return "[%s] %s" % (self.date, self.name)


class Event(db.Model):
    date     = db.DateTimeProperty(auto_now_add=True)
    client   = db.ReferenceProperty(Client)
    category = db.ReferenceProperty(Category)
    ip       = db.StringProperty()
    data     = db.TextProperty()

    def __str__(self):
        return "[%s] %s (%s): %s - %s" % (self.date, self.client, self.ip,
                self.category, self.data)

    @property
    def short_detail(self):
        mod = getattr(parsers, self.category.name)
        return mod.short_detail(self.data)

    @property
    def full_detail(self):
        mod = getattr(parsers, self.category.name)
        return mod.full_detail(self.data)

    @property
    def alert_color(self):
        delta = datetime.datetime.utcnow() - self.date
        if delta.seconds < 300:
            color = '#52FFB9'
        elif delta.seconds < 600:
            color = '#F7F28E'
        else:
            color = '#FF8C6D'
        return color


# ########################
# Views
# ########################

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and user.nickname() not in USERS:
            self.error(403)
        else:
            self.redirect(users.create_login_url(self.request.uri))

        events = Event.all()
        clients = Client.all()
        categories = Category.all()

        if self.request.get('client'):
            events.filter('client = ', db.Key(self.request.get('client')))
        if self.request.get('category'):
            events.filter('category = ', db.Key(self.request.get('category')))
       
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
        if not client:
            self.error(400)
            self.response.headers.add_header('Error-Message',
                    'Missing client id.')
        else:
            cli = Client.get_or_insert(client, name=client)
            cat = Category.get_or_insert(category, name=category)
            event = Event(client=cli, category=cat, ip=self.request.remote_addr)
            if self.request.get('data'):
                event.data = self.request.get('data')
            event.put()


# ########################
# App stuff 
# ########################

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
