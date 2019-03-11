import unittest
from unittest import TestCase
from com.direqlink.migration.credentials import Credentials
from com.direqlink.migration.connector import Connection
from com.direqlink.migration.migrator import Migration, Workload, MigrationTarget, MigrationException
from com.direqlink.migration.constants import MigrationState, CloudType
from com.direqlink.migration.mountpoint import MountPoint

class TestMigration(TestCase):
	def test_init_no_args(self):
		migration = Migration()
		self.assertIsNone(migration.source)
		self.assertIsNone(migration.target)
		self.assertEquals(migration.state, MigrationState.NOT_DEFINED)
		
	def test_init_partial_args(self):
		source_ip = "10.92.248.123"
		source_username = "lucky"
		source_password = "12345678" # poorest password ever
		source_domain = "ASIA"
		
		source_credentials = Credentials(source_username, source_password, source_domain)
		source = Workload(source_ip)
		source.set_credentials(source_credentials)
		
		migration = Migration(source)
		self.assertEquals(migration.source, source)
		self.assertIsNone(migration.target)
		self.assertEquals(migration.state, MigrationState.NOT_DEFINED)
		
	def test_init_target_vm_missing(self):
		source_ip = "10.92.248.123"
		source_username = "lucky"
		source_password = "12345678" # poorest password ever
		source_domain = "ASIA"
		
		source_credentials = Credentials(source_username, source_password, source_domain)
		source = Workload(source_ip)
		source.set_credentials(source_credentials)
		
		target_ip = "221.122.34.23"
		target_username = "lucky_azure"
		target_password = "abcdefgh" # another poorest password ever
		target_domain = "AMER"
		
		target_credentials = Credentials(target_username, target_password, target_domain)
		target_vm = Workload(target_ip)
		target_vm.set_credentials(target_credentials)
		
		target = MigrationTarget(cloud_type=CloudType.AZURE)
		#target.set_target_vm(target_vm)
	
		migration = Migration(source, target)
		
		self.assertEquals(migration.source, source)
		self.assertEquals(migration.target, target)
		self.assertEquals(migration.state, MigrationState.NOT_DEFINED)
		
	def test_init_full_args(self):
		source_ip = "10.92.248.123"
		source_username = "lucky"
		source_password = "12345678" # poorest password ever
		source_domain = "ASIA"
		
		source_credentials = Credentials(source_username, source_password, source_domain)
		source = Workload(source_ip)
		source.set_credentials(source_credentials)
		
		target_ip = "221.122.34.23"
		target_username = "lucky_azure"
		target_password = "abcdefgh" # another poorest password ever
		target_domain = "AMER"
		
		target_credentials = Credentials(target_username, target_password, target_domain)
		target_vm = Workload(target_ip)
		target_vm.set_credentials(target_credentials)
		
		target = MigrationTarget(cloud_type=CloudType.AZURE)
		target.set_target_vm(target_vm)
	
		migration = Migration(source, target)
		
		self.assertEquals(migration.source, source)
		self.assertEquals(migration.target, target)
		self.assertEquals(migration.state, MigrationState.NOT_STARTED)
		
	def test_add_mountpoint(self):
		source_ip = "10.92.248.123"
		source_username = "lucky"
		source_password = "12345678" # poorest password ever
		source_domain = "ASIA"
		
		source_credentials = Credentials(source_username, source_password, source_domain)
		source = Workload(source_ip)
		source.set_credentials(source_credentials)
		source.set_storage_list([MountPoint("C:\\",3785863),MountPoint("D:\\",3785863)])
		
		target_ip = "221.122.34.23"
		target_username = "lucky_azure"
		target_password = "abcdefgh" # another poorest password ever
		target_domain = "AMER"
		
		target_credentials = Credentials(target_username, target_password, target_domain)
		target_vm = Workload(target_ip)
		target_vm.set_credentials(target_credentials)
		
		target = MigrationTarget(cloud_type=CloudType.AZURE)
		target.set_target_vm(target_vm)
	
		migration = Migration(source, target)
		
		self.assertEquals(len(migration.source.storage), 2)
		
		with self.assertRaises(MigrationException):
			migration.add_mountpoint(MountPoint("E:\\", 837579))
		self.assertEquals(len(migration.selected_mountpoints), 0)
		
		migration.add_mountpoint(MountPoint("D:\\", 837579))
		self.assertEquals(len(migration.selected_mountpoints), 1)
		
		self.assertEquals(migration.state, MigrationState.NOT_STARTED)
		
if __name__ == "__main__":
	unittest.main()

