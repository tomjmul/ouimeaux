import abc
from yapsy.IPlugin import IPlugin

class Plugin(object):

	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	def initialise(self, configuration):
		raise NotImplementedError	

	@abc.abstractmethod
	def handle_event(self, data):
		raise NotImplementedError

	@abc.abstractproperty
	def name(self):
		raise NotImplementedError

