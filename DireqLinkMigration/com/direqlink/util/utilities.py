class EnumUtil(object):
	@staticmethod
	def enum_from_value(value, enum):
		for item in enum:
			if item.value == value:
				return item
		return None