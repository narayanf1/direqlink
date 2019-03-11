import unittest
from unittest import TestCase
from com.direqlink.migration.credentials import Credentials
from com.direqlink.migration.connector import Connection

class TestConnection(TestCase):
	def test_connection(self):
		host = "127.0.0.1"
		credentials = Credentials("lucky", "P@ssw0rd", "ASIA")
		
		with Connection(host, credentials) as connection:
			self.assertTrue(isinstance(connection, Connection.OSConnection))
			
			file_path = "C:\\"
			self.assertTrue(isinstance(connection.read_file(file_path), object))
			self.assertTrue(isinstance(connection.list_dir(file_path), list))
			self.assertTrue(connection.is_dir("C:\\", "Lucky"))
			self.assertFalse(connection.is_dir("C:\\", "Temp\\abc.def"))

if __name__ == "__main__":
	unittest.main()
