import unittest
from unittest import TestCase
from com.direqlink.migration.credentials import Credentials, CredentialsException

class TestCredentials(TestCase):
	def test_credentials_fail(self):
		with self.assertRaises(CredentialsException):
			credentials = Credentials("lucky", "P@ssw0rd", None)
		
		credentials = Credentials("lucky", "P@ssw0rd", "ASIA")
		self.assertIsNotNone(credentials)

if __name__ == "__main__":
	unittest.main()
