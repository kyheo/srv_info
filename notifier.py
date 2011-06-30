import urllib
import optparse

import parsers

# Usage example
# python notifier.py --name=nibbler --add=ping --param= --add=ip --param=lo,wlan0,eth0

# Options
# python notifier.py -h
parser = optparse.OptionParser()
parser.add_option('--name', type='string', dest='name', help='''Client name''')
parser.add_option('--host', type='string', dest='host', default='localhost', 
        help='''Host to where the notification should be sent.''')
parser.add_option('--port', type='string', dest='port', default="8080",
        help='''Port to where the notification should be sent.''')
parser.add_option('--add', type='string', dest='categories', action='append',
        help='Category to notify (Multiple).')
parser.add_option('--param', type='string', dest='params', action='append', 
        help='''For each category added, a param must be added. It is a list, so
first param relates to first category.''')
(options, args) = parser.parse_args()

# Process
url = 'http://%s:%s/notify/%s/%%s' % (options.host, options.port, options.name)

for i in range(len(options.categories)):
    fn = getattr(parsers, options.categories[i])
    data = fn.get_from_system(options.params[i])
    data = urllib.urlencode({'data': data})
    urllib.urlopen(url % (options.categories[i],), data=data)
