import os
import yaml

from configure import Configuration


def in_home(*path):
    try:
        from win32com.shell import shellcon, shell
    except ImportError:
        home = os.path.expanduser("~")
    else:
        home = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    return os.path.join(home, *path)


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


class WemoConfiguration(object):
    def __init__(self, filename=None):
        if filename is None:
            ensure_directory(in_home('.wemo'))
            filename = in_home('.wemo', 'config.yml')
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write("""
aliases:
# Shortcuts to longer device names. Uncommenting the following
# line will allow you to execute 'wemo switch lr on' instead of
# 'wemo switch "Living Room Lights" on'
#
#    lr: Living Room Lights

# ip:port to bind to when receiving responses from discovery.
# The default is first DNS resolution of local host, port 54321
#
# bind: 10.1.2.3:9090

# Web app bind address
#
# listen: 0.0.0.0:5000

# Require basic authentication (username:password) for the web app
#
# auth: admin:password
""")
        with open(filename, 'r') as cfg:
            self.config = Configuration.from_file(filename).configure()

    @property
    def aliases(self):
        return self.config.get('aliases', {})

    @property
    def bind(self):
        return self.config.get('bind', None)

    @property
    def listen(self):
        return self.config.get('listen', None)

    @property
    def auth(self):
        return self.config.get('auth', None)

    @property
    def plugins_directory(self):
        return self.config.get('pluginsDirectory', {})

    @property
    def plugins(self):
        return self.config.get('plugins', {})
