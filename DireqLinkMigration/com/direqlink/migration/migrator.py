from .constants import MigrationState
from .connector import Connection
import time

class MigrationException(Exception):
	pass
	
class Workload(object):
	""" Represents the migration source
		This takes the source IP address, credentials object and a list of storage spaces (C:\, D:\, etc)
	"""
	
	def __init__(self, ip):
		# ip is immutable.  since Python doesn't support private variables, prepending this with double underscores.
		self.__ip = ip
		self.credentials = None
		self.storage = []
	
	def set_credentials(self, credentials):
		self.credentials = credentials
	
	def set_storage_list(self, storage_list):
		self.storage = storage_list
		
	def get_ip(self):
		return self.__ip
		
class MigrationTarget(object):
	""" Represents the migration target (cloud)
		This takes the cloud type and a target_vm which is of type Workload
	"""
	
	def __init__(self, cloud_type):
		self.cloud_type = cloud_type
		self.target_vm = None
	
	def set_target_vm(self, target_vm):
		self.target_vm = target_vm

class Migration(object):
	""" The central class of the migration system.
		
		Initiate a migration object by supplying optional source and target objects.
		However, if source and target are not provided during initialization, 
			use setter methods to set them before starting migration.
		
	"""
	
	def __init__(self, source=None, target=None):
		self.selected_mountpoints = []
		self.source = source
		self.target = target
		
		# migration state remains in NOT_DEFINED until source and target objects are defined,
		# including their attributes.
		# once set, the state moves into NOT_STARTED.
		if not ((self.source and self.source.credentials) \
				and (self.target and self.target.target_vm and self.target.target_vm.credentials)):
			self.state = MigrationState.NOT_DEFINED
		else:
			self.state = MigrationState.NOT_STARTED
		
	def set_source(self, source):
		self.source = source
		
		if (self.source and self.source.credentials) \
				and (self.target and self.target.target_vm and self.target.target_vm.credentials):
			self.state = MigrationState.NOT_STARTED
		
	def set_target(self, target):
		self.target = target
		
		if (self.source and self.source.credentials) \
				and (self.target and self.target.target_vm and self.target.target_vm.credentials):
			self.state = MigrationState.NOT_STARTED
	
	def add_mountpoint(self, mountpoint):
		""" Add the mountpoints selected for migration.
			Pre-condition: The mountpoint being selected should be present in the source as a storage.
		"""
		if mountpoint not in self.source.storage:
			raise MigrationException("Mountpoint {} not defined in source system".format(mountpoint.name))
			
		self.selected_mountpoints.append(mountpoint)
		
	def run(self):
		""" Runs the migration process.
			Pre-condition: The source and target objects need to be defined including their attributes.
							Which in turn means the current state should be NOT_STARTED
		"""
		
		print "***Migration State: {}".format(self.state)
		
		# state check
		if self.state == MigrationState.NOT_DEFINED:
			raise MigrationException("Source/Target are not defined")
			
		elif self.state == MigrationState.RUNNING:
			raise MigrationException("Migration is in RUNNING state")
		
		# in real-world we should be able to re-run however, for simplicity we will stop if in these states.
		elif self.state in (MigrationState.SUCCESS, MigrationState.ERROR):
			raise MigrationException("Migration is already run and resulted in {} state".format(self.state.name))
			
		# if we reach here it means the state is NOT_STARTED and we're good to proceed
		# Step 1: establishing mocked source and target connections
		with Connection(self.source.get_ip(), self.source.credentials) as source_connection, \
				Connection(self.target.target_vm.get_ip(), self.target.target_vm.credentials) as target_connection:
				
			# Step 2: change to RUNNING state
			self.state = MigrationState.RUNNING
			print "***Migration State: {}".format(self.state)
			
			# Step 3: Loop over each of the selected mountpoints
			for mountpoint in self.selected_mountpoints:
				try:
					# Step 4: get a recursive list of files and folders in the mount point (mocked list)
					for file_path in source_connection.list_dir(mountpoint.name):
					
						# Step 5.1: create directory on target
						if source_connection.is_dir(mountpoint.name, file_path):
							target_connection.mkdir(file_path)
						else:
							# Step 5.2: read file from source and write on target (in real-world a lot more would happen here)
							time.sleep(2) # simulating read and write time
							file_content = source_connection.read_file(file_path)
							target_connection.write_file(path=file_path, content=file_content)
							
					# Step 6: After all selected mountpoints are migrated, change state to SUCCESS.
					self.state = MigrationState.SUCCESS
				except Exception as e:
					# In the event of any error, change state to ERROR.
					# With our mocked data, we're assuming only Access related error.
					print "Access denied for mountpoint {}. Exception: {}".format(mountpoint.name, str(e))
					self.state = MigrationState.ERROR
					
			print "***Migration State: {}".format(self.state)
