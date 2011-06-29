import logging

import socket
import fcntl
import struct


def short_detail(data):
    return ' / '.join([str(v) for k, v in data.iteritems()])


def full_detail(data):
    return '\n'.join(['%s: %s' % (k, v) for k, v in data.iteritems()])


def get_from_system(params):
    data = {}
    for ifname in params['interfaces']:
        data[ifname] = _get_ip_address(ifname)
    return data


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
