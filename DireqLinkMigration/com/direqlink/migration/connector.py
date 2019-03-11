from test.com.direqlink.migration import test_data

class FileSystemPermissionException(Exception):
	pass
	
class Connection(object):
	""" A context manager to establish a connection with a machine (local or cloud)
	
		The context manager returns an internal OSConnection object.
		This OSConnection object provides various machine-level file operation APIs.
		These APIs are appropriately mocked (return sample data where applicable).
	"""
	class OSConnection(object):
		def __init__(self):
			pass
			
		def read_file(self, path):
			file_content = object() # mock the data
			try:
				print "reading file: {}".format(path)
			except Exception as e:
				# assume this is a permission issue
				raise FileSystemPermissionException("User does not have permission to resource: {}".format(path))
				
			return file_content
			
		def write_file(self, path, content):
			print "writing file: {}".format(path)
			
		def list_dir(self, path):
			file_list = []
			try:
				file_list = [file_path for file_path in test_data.FILE_LIST[path]]
				print "Recursively listing directory: {}".format(path)
			except Exception as e:
				# assume this is a permission issue
				raise FileSystemPermissionException("User does not have permission to resource: {}".format(path))
				
			return file_list
			
		def is_dir(self, root, path):
			return test_data.FILE_LIST[root][path] == test_data.FileType.FOLDER
			
		def mkdir(self, path):
			print "Creating directory: {}".format(path)

			
	def __init__(self, host, credentials):
		self.host = host
		self.credentials = credentials
		self.connection = None
		
	def __enter__(self):
		# in real-world establish a connection to the host
		self.connection = Connection.OSConnection()
		return self.connection
		
	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type:
			print "Exception connecting to host"
		else:
			# in real-world call close method on the connection
			self.connection = None
		
