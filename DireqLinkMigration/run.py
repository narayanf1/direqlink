from com.direqlink.migration.migrator import Workload, MigrationTarget, Migration
from com.direqlink.migration.mountpoint import MountPoint
from com.direqlink.migration.credentials import Credentials
from com.direqlink.migration.constants import CloudType

def run_migrator():
	""" This is a command-line based application runner.
	
		Think of this as a tester for the application with certain scenarios simulated.
		Refer to the rest_runner.py which provides RESTful services for interactive API calls.
	"""
	
	# let's setup the source workload first
	source_ip = "10.92.248.123"
	source_username = "lucky"
	source_password = "12345678" # poorest password ever
	source_domain = "ASIA"
	
	source_credentials = Credentials(source_username, source_password, source_domain)
	source = Workload(source_ip)
	source.set_credentials(source_credentials)
	
	storage_list = [MountPoint("C:\\", 238590), MountPoint("D:\\", 43785638)]
	source.set_storage_list(storage_list)
	
	# now setup target
	target_ip = "221.122.34.23"
	target_username = "lucky_azure"
	target_password = "abcdefgh" # another poorest password ever
	target_domain = "AMER"
	
	target_credentials = Credentials(target_username, target_password, target_domain)
	target_vm = Workload(target_ip)
	target_vm.set_credentials(target_credentials)
	
	target = MigrationTarget(cloud_type=CloudType.AZURE)
	target.set_target_vm(target_vm)
	
	# time to run migration
	migration = Migration(source, target)
	migration.add_mountpoint(MountPoint("C:\\", 238590))
	migration.run()

if __name__ == "__main__":
	run_migrator()