import logging
import json

import socket
import fcntl
import struct


def short_detail(data):
    data = json.loads(data)
    return ' / '.join([str(v) for k, v in data.iteritems()])


def full_detail(data):
    data = json.loads(data)
    return '\n'.join(['%s: %s' % (k, v) for k, v in data.iteritems()])


def get_from_system(params):
    params = params.split(',')
    data = {}
    for ifname in params:
        data[ifname] = _get_ip_address(ifname)
    return json.dumps(data)


def _get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except IOError, e:
        pass
