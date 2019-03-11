class MountPointException(Exception):
	pass
	
class MountPoint(object):
	def __init__(self, name, size):
		if not all((name, size)):
			raise MountPointException("Name and volume size are mandatory to define a MountPoint.")
			
		self.name = name
		self.size = size
	
	def __hash__(self):
		return hash(self.name)
		
	def __eq__(self, other):
		""" Determines equalness based on the name of the mountpoint
		"""
		
		if not isinstance(other, MountPoint):
			return False
		return self.name == other.name