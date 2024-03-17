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
        ms = (end-start)*100

        if method.__name__ == "__init__":
        	print(f"Data collected: {int(ms)}ms")
        elif method.__name__ == "get_messages":
        	print(f"Data organised: {int(ms)}ms")
        elif method.__name__ == "output":
        	print(f"Data outputted: {int(ms)}ms")

        return result
    return wrapper


class Data:
	version = "v1.0.0"

	@timer
	def __init__(self,directory):
		self.directory = directory
		files = glob.glob(f"{directory}/*")
		data = []

		for item in files:
			if "." in item: # ignores files
				continue

			file_dir = os.path.join(directory,item,"messages.json")

			if not (os.path.exists(file_dir)): # ignores other folders
				continue

			with open(file_dir,"r") as f: # collecting the json data (file_name/messages.json)
				try:
					d = json.load(f)
					for x in d: # checking all the expected key
						x["Contents"]
						x["Attachments"]
						x["ID"]
						x["Timestamp"]
				except:
					print(f"Warrning: Unexpected json Syntax at {file_dir}")
					continue
				data.append(d)

		if not data:
			print(f"Error: Data not Found, check if the data directory is correct\nDirectory: {directory}\n")
			sys.exit(1)

		self.data = data



	@timer
	def get_messages(self,key="",limit=-1,st=True,reverse=False,attachment=False):
		messages = []
		tm = []

		# limit: -1 = all
		if limit == -1:
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
						messages.append(message)
						tm.append(item["Timestamp"])

		if st and messages:						
			tm,messages = zip(*sorted(zip(tm,messages),reverse=reverse)) # messages sorted by timestamp

		return tm,messages 


	@staticmethod
	def valid_fname(name,directory): 
		# checking if the file name is valid
		# or making another file with index (name1, name2, name3, ... , nameX)
		n = name
		s = 2

		file_dir = os.path.join(directory,n+".txt")
		while os.path.exists(file_dir): 
			n = name
			n += str(s)
			s +=1
			file_dir = os.path.join(directory,n+".txt")

		return n


	@timer
	def output(self,time,messages,name,directory="",index=False,timestamps=True,console=False):
		name = Data.valid_fname(name,directory)
		string = ""

		for i in range(len(messages)): # messages per line
			if index:
				string += str(i+1)
				string += ". "
			if timestamps:
				string += time[i]
				string += ": "
			string += messages[i]+"\n"

		if console:
			print(string)
		else:
			file_dir = os.path.join(directory,name+".txt")
			try:
				with open(file_dir,"w") as f:
					try:
						f.write(string)
					except (IOError, OSError):
						print("Error: There was an error writing to the file")
			except (FileNotFoundError, PermissionError, OSError):
				print(f"Error: There was an error while opening the file, check the output directory {directory}")
				sys.exit(1)