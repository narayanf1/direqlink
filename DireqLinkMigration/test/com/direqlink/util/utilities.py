import unittest
from unittest import TestCase
from com.direqlink.migration.constants import CloudType
from com.direqlink.util.utilities import EnumUtil

class TestEnumUtil(TestCase):
	def test_enum_from_value(self):
		self.assertIsNone(EnumUtil.enum_from_value("alas", CloudType))
		self.assertEquals(EnumUtil.enum_from_value("azure", CloudType), CloudType.AZURE)
		
if __name__ == "__main__":
	unittest.main()
