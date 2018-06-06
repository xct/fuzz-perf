''' Implement your driver for your own fuzzer here.	By convention it must write its 
	outputs (which are expected to be inputs to the target program) to results/<fuzzername>/<projectname>/<binaryname>/queue. 
	Easiest way to start is the class of another fuzzer and modify it.
'''

class AFL():

	def __init__(self):		
		self.name = "afl"

	def pre(self, project, binary, args):
		self.project = project
		self.binary = binary
		self.args = args
		cmd = "mkdir -p results/afl/"+self.project+"/"+self.binary+" && "
		cmd += "../afl/afl-fuzz -i seeds/ -o results/afl/"+self.project+"/"+self.binary+" -Q -m none targets/"+self.project+"/"+self.binary+" "+''.join(self.args)
		return cmd

	def post(self):
		results = "results/"+self.name+"/"+self.project+"/"+self.binary
		cmd = "cp "+results+"/crashes/id* "+results+"queue/" # copy crashes to queue too
		return cmd


class Pathfinder():
	
	def __init__(self):		
		self.name = "Pathfinder"

	def pre(self, project, binary, args):
		self.project = project
		self.binary = binary
		self.args = args
		cmd = "cd ../pathfinder/ && "
		cmd += "python fuzzer.py -i ../fuzz-perf/seeds/ "
		cmd += "\"../fuzz-perf/targets/"+self.project+"/"+self.binary+" "+''.join(self.args)+"\""
		print(cmd)
		return cmd

	def post(self):		
		results = "results/"+self.name+"/"+self.project+"/"+self.binary+""
		cmd = "mkdir -p "+results+"/queue/"
		cmd += "; rm "+results+"/*"
		cmd += "; rm "+results+"/queue/*"
		cmd += "; cp ../tmp/pathfinder/"+self.binary+"/queue/* "+results+"/queue/"
		return cmd
