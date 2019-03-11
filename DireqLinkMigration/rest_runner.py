from flask import Flask, request, jsonify
from com.direqlink.migration.migrator import Workload, MigrationTarget, Migration
from com.direqlink.migration.credentials import Credentials
from com.direqlink.migration.mountpoint import MountPoint
from com.direqlink.migration.constants import CloudType
from com.direqlink.util.utilities import EnumUtil
from threading import Thread
import json

app = Flask(__name__)
migration = Migration()

@app.route("/", methods=["GET"])
def home():
	""" Returns the content for index page.
	
		Lists the available services.
		POST calls need the values with names mentioned in the brackets.
		
		Refer to curl.txt for samples.
	"""
	return """<h1>Welcome to DireqLink Data Migration</h1><br/>
				<p>Following endpoints are available</p>
				<ul>
					<li>[POST] 		register-source(ip, username, password, domain, storage_list)</li>
					<li>[POST] 		register-target(ip, username, password, domain, cloud_type)</li>
					<li>[POST] 		add-mountpoint(name, size)</li>
					<li>[GET] 		selected-mountpoints()</li>
					<li>[GET/POST] 	start-migration()</li>
					<li>[GET]  		migration-status()</li>
				</ul>
			""", 200

@app.route("/register-source", methods=["POST"])
def register_source():
	""" Creates a source object for the migration with the supplied parameters
	"""
	
	request_data	= json.loads(request.data)
	ip 				= request_data.get("ip")
	username 		= request_data.get("username")
	password 		= request_data.get("password")
	domain 			= request_data.get("domain")
	storage_list 	= request_data.get("storage_list", [])
	try:
		source_credentials = Credentials(username, password, domain)
		source = Workload(ip)
		source.set_credentials(source_credentials)
		
		storage_list_mountpoints = []
		for storage in storage_list:
			mountpoint = MountPoint(storage["name"], storage["size"])
			storage_list_mountpoints.append(mountpoint)
		
		source.set_storage_list(storage_list_mountpoints)
		migration.set_source(source)
		
		return jsonify({"status":"success", "message":"source has been defined"}), 201
	except Exception as e:
		return jsonify({"status":"failure", "message":str(e)}), 406

@app.route("/register-target", methods=["POST"])
def register_target():
	""" Creates a target object for the migration with the supplied parameters
	"""
	
	try:
		request_data	= json.loads(request.data)
		ip 				= request_data.get("ip")
		username 		= request_data.get("username")
		password 		= request_data.get("password")
		domain 			= request_data.get("domain")
		cloud_type 		= request_data.get("cloud_type")
		
		cloud_type_enum = EnumUtil.enum_from_value(cloud_type, CloudType)
		
		target_credentials = Credentials(username, password, domain)
		target_vm = Workload(ip)
		target_vm.set_credentials(target_credentials)
		
		target = MigrationTarget(cloud_type)
		target.set_target_vm(target_vm)
		
		migration.set_target(target)
		
		return jsonify({"status":"success", "message":"target has been defined"}), 201
	except Exception as e:
		return jsonify({"status":"failure", "message":str(e)}), 406

@app.route("/add-mountpoint", methods=["POST"])
def add_mountpoint():
	""" Add a mountpoint selection for migration.
	"""
	
	try:
		if not migration.target:
			raise Exception("Target has not yet been defined")
			
		request_data	= json.loads(request.data)
		name 			= request_data.get("name")
		size 			= request_data.get("size")
		
		mountpoint = MountPoint(name, size)
		migration.add_mountpoint(mountpoint)
		
		return jsonify({"status":"success", "message":"MountPoint {} has been added".format(name)}), 201
	except Exception as e:
		return jsonify({"status":"failure", "message":str(e)}), 406

@app.route("/selected-mountpoints", methods=["GET"])
def selected_mountpoints():
	""" Get the list of mountpoints selected for migration
	"""
	
	return jsonify({"status":"success", "mountpoints":migration.selected_mountpoints}), 200

@app.route("/start-migration", methods=["GET", "POST"])
def start_migration():
	""" Invokes the run method on the migration object
	"""
	
	try:
		if not (migration.source and migration.target):
			raise Exception("Source and/or Target have not yet been defined")
			
		if not migration.selected_mountpoints:
			raise Exception("No mountpoint has been selected")
			
		Thread(target=migration.run).start()
		
		return jsonify({"status":"success", "message":"Migration has been started"}), 202
	except Exception as e:
		return jsonify({"status":"failure", "message":str(e)}), 406

@app.route("/migration-state", methods=["GET"])
def migration_state():
	""" Gets the current state of migration
	"""
	
	return jsonify({"status":"success", "migration_state":"{} - {}".format(migration.state.name, migration.state.value)}), 200

if __name__=="__main__":
	app.run()