from enum import Enum
from collections import OrderedDict

class FileType(Enum):
	FOLDER 	= "folder"
	FILE	= "file"

# Maintaining a dictionary to simulate real OS like file attributes	
FILE_LIST = {
	"C:\\" : OrderedDict()
}
FILE_LIST["C:\\"]["Temp"] = FileType.FOLDER
FILE_LIST["C:\\"]["Lucky"] = FileType.FOLDER
FILE_LIST["C:\\"]["Temp\\abc.def"] = FileType.FILE
FILE_LIST["C:\\"]["Temp\\tmp_folder"] = FileType.FOLDER
FILE_LIST["C:\\"]["Temp\\tmp_folder\\.hidden"] = FileType.FILE
FILE_LIST["C:\\"]["Lucky\\Python"] = FileType.FOLDER
FILE_LIST["C:\\"]["Lucky\\Python\\test.py"] = FileType.FILE
FILE_LIST["C:\\"]["Lucky\\Python\\__init__.py"] = FileType.FILE
FILE_LIST["C:\\"]["Lucky\\profile.txt"] = FileType.FILE
