import unittest
from unittest import TestCase
from com.direqlink.migration.mountpoint import MountPoint, MountPointException

class TestMountPoint(TestCase):
	def test_init(self):
		with self.assertRaises(MountPointException):
			mountpoint = MountPoint("", 83475)
		
		mountpoint = MountPoint("C:\\", 83475)
		self.assertIsNotNone(mountpoint)

	def test_equals(self):
		mountpoint1 = MountPoint("C:\\", 83475)
		mountpoint2 = MountPoint("C:\\", 35334)
		self.assertEquals(mountpoint1, mountpoint2)
		
if __name__ == "__main__":
	unittest.main()
