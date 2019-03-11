from enum import Enum

class CloudType(Enum):
	AWS 	= "aws"
	AZURE 	= "azure"
	VSPHERE	= "vsphere"
	VCLOUD	= "vcloud"
	
class MigrationState(Enum):
	NOT_DEFINED = "Source and/or Target not defined"
	NOT_STARTED	= "Migration not started"
	RUNNING		= "Migration is in progress"
	SUCCESS		= "Migration completed successfully"
	ERROR		= "An error occurred during migration"
