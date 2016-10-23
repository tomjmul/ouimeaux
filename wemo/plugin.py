import abc
from yapsy.IPlugin import IPlugin

class Plugin(IPlugin):

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def print_name(self):
		pass
