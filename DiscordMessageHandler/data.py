import sys
import glob
import json
import time
import os


# benchmarking 
def timer(method):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        ms = (end-start)*1000
        if method.__name__ == "__init__":
        	print(f"Data collected: {int(ms)}ms")
        elif method.__name__ == "get_messages":
        	print(f"Data organised: {int(ms)}ms")
        elif method.__name__ == "output":
        	print(f"Data outputted: {int(ms)}ms")
        else:
        	print(f"{method.__name__}: {int(ms)}ms")
        return result
    return wrapper


class Data:
	version = "v1.1.0"

	@timer
	def __init__(self,directory):
		self.directory = directory
		self.data = self.get_data(directory)
		self.messages = []
		self.timestamps = []


	@timer
	def get_messages(self,key="",limit=-1,st=True,reverse=False,attachment=False):
		"""Retrieve and optionally sort messages based on provided parameters."""
		if limit == -1: # limit: -1 = all
			limit = len(self.data)

		for i in range(limit): # running data per folder
			for item in self.data[i]: # running data per message
				if not attachment:
					message = item["Contents"]
				else:
					message = item["Attachments"]
					key = "" # attachments can't have key

				if message: 
					if key in message:
						self.messages.append(message)
						self.timestamps.append(item["Timestamp"])

		if st and self.messages:						
			self.timestamps,self.messages = zip(*sorted(zip(self.timestamps,self.messages),reverse=reverse)) # messages sorted by timestamp


	@timer
	def output(self,name,directory="",index=False,time=True,console=False):
		"""Output messages to a file or console based on provided parameters."""
		name = self.valid_fname(name,directory)
		string = self.messages_to_string(index,time)

		if console:
			print(string)
		else:
			file_dir = os.path.join(directory,name+".txt")
			self.write_data(string,file_dir)


	def messages_to_string(self,index=True,time=True):
		"""Convert messages to a formatted string."""
		string = ""
		for i in range(len(self.messages)): # messages per line
			if index:
				string += str(i+1)
				string += ". "
			if time:
				string += self.timestamps[i]
				string += ": "
			string += self.messages[i]+"\n"
		return string


	@staticmethod
	def write_data(string,directory):
		"""Write the provided string to a file."""
		try:
			with open(directory,"w") as f:
				try:
					f.write(string)
				except (IOError, OSError):
					print("Error: There was an error writing to the file")
		except (FileNotFoundError, PermissionError, OSError):
			print(f"Error: There was an error while opening the file, check the output directory {directory}")
			sys.exit(1)


	@staticmethod
	def valid_data(name,directory):
		 """Validate and return JSON data from the specified directory."""
		 if "." in name: # ignores file
		 	return {}

		 file_dir = os.path.join(directory,name,"messages.json")

		 if not (os.path.exists(file_dir)): # ignores other folders
		 	return {}

		 with open(file_dir,"r") as f: # collecting the json data (file_name/messages.json)
		 	try:
		 		jdata = json.load(f)
		 		for x in jdata: # checking for all the expected keys
		 			x["Contents"]
		 			x["Attachments"]
		 			x["ID"]
		 			x["Timestamp"]
		 	except(KeyError,json.JSONDecodeError):
		 		print(f"Warning: Unexpected json Syntax at {file_dir}")
		 		return {}

		 return jdata


	@staticmethod
	def get_data(directory):
		"""Retrieve and validate all JSON data from the specified directory."""
		data = []
		files = glob.glob(f"{directory}/*")

		for item in files:
			fdata = Data.valid_data(item,directory)
			data.append(fdata)

		if not data:
			print(f"Error: Data not found, check if the data directory is correct\nDirectory: {directory}")
			sys.exit(1)

		return data


	@staticmethod
	def valid_fname(name,directory): 
		"""Generate a valid file name, ensuring no conflicts with existing files."""
		n = name
		s = 2

		file_dir = os.path.join(directory,n+".txt")
		while os.path.exists(file_dir): 
			n = name
			n += str(s)
			s +=1
			file_dir = os.path.join(directory,n+".txt")

		return n