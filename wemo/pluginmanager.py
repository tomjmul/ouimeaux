import logging
import time

from wemo.signals import statechange
from .config import WemoConfiguration
from yapsy.PluginManager import PluginManager as PluginFramework

log = logging.getLogger(__name__)

manager = PluginFramework()

class PluginManager:

  def __init__(self):
    logging.basicConfig(level=logging.INFO)
    config = WemoConfiguration()
    if config.plugins_directory:
      log.info("Plugins directory is configured as {} - loading plugins".format(config.plugins_directory))
      self.plugins = (config.plugins or {})
      log.info("Found configuration for plugins: {}".format(self.plugins.keys()))
      manager.setPluginPlaces([config.plugins_directory])
      manager.collectPlugins()
      # Loop round the plugins and print their names.
      for plugin in manager.getAllPlugins():
        name = plugin.plugin_object.name
        log.info("Found plugin: {}".format(name))
        config = {}
        if (name in self.plugins):
          log.info("Loading plugin: {}".format(name))
          config = self.plugins.get(name)
          log.info("Initialising plugin {} with config: {}".format(name, config))
          plugin.plugin_object.initialise(config)
          manager.activatePluginByName(plugin.name)
        else:
          log.info("Skipping plugin: {} - not configured".format(name))
    else:
      log.info("Plugins directory is not configured - skipping plugins")

  def delegate_event(self, sender, **kwargs):
    data = sender.serialise()
    data['state'] = kwargs.get('state', data['state'])
    data['timestamp'] = timestamp = int(time.time())
    for plugin in manager.getAllPlugins():
      name = plugin.plugin_object.name
      if (name in self.plugins):
        plugin.plugin_object.handle_event(data)

  def start(self):
    statechange.connect(self.delegate_event,
                        dispatch_uid=id(self))

  def __del__(self):
    statechange.disconnect(dispatch_uid=id(self))
