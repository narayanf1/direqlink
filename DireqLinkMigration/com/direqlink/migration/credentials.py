class CredentialsException(Exception):
	pass
	
class Credentials(object):
	def __init__(self, username, password, domain):
		if not all((username, password, domain)):
			raise CredentialsException("username, password and domain are mandatory to build Credentials.")
			
		self.__username = username
		self.__password = password
		self.__domain = domain
