''' Implement your driver for your own fuzzer here.	By convention it must write its 
	outputs (which are expected to be inputs to the target program) to results/<fuzzername>/<projectname>/<binaryname>/queue. 
	Easiest way to start is the class of another fuzzer and modify it.
'''

class AFL():

	def __init__(self):		
		self.name = "afl"

	def pre(self, project, binary, args):
		''' Prepare environment and run the fuzzer
		'''
		self.project = project
		self.binary = binary
		self.args = args
		results = "results/"+self.name+"/"+self.project+"/"+self.binary
		cmd = "mkdir -p "+results+" && "
		cmd += "../afl/afl-fuzz -i seeds/ -o "+results+" -Q -m none targets/"+self.project+"/"+self.binary+" "+''.join(self.args)
		return cmd

	def post(self):
		''' Copy results to correct folder & do necessary cleanup 
		'''
		results = "results/"+self.name+"/"+self.project+"/"+self.binary
		cmd = "cp "+results+"/crashes/id* "+results+"queue/" # copy crashes to queue too
		return cmd

	def crashes(self):
		''' number of crashes
		'''
		results = "results/"+self.name+"/"+self.project+"/"+self.binary
		cmd = "ls -1 "+results+"/crashes/ | grep -iv 'Readme' | wc -l "
		return cmd


class Pathfinder():
	
	def __init__(self):		
		self.name = "pathfinder"

	def pre(self, project, binary, args):
		''' Prepare environment and run the fuzzer
		'''
		self.project = project
		self.binary = binary
		self.args = args
		cmd = "cd ../pathfinder/ && "
		cmd += "python fuzzer.py -i ../fuzz-perf/seeds/ "
		cmd += "\"../fuzz-perf/targets/"+self.project+"/"+self.binary+" "+''.join(self.args)+"\""
		print(cmd)
		return cmd

	def post(self):	
		''' Copy results to correct folder & do necessary cleanup 
		'''	
		results = "results/"+self.name+"/"+self.project+"/"+self.binary+""
		cmd = "mkdir -p "+results+"/queue/"
		cmd += "; rm "+results+"/*"
		cmd += "; rm "+results+"/queue/*"
		cmd += "; cp ../tmp/pathfinder/"+self.binary+"/queue/* "+results+"/queue/"
		return cmd

	def crashes(self):
		''' number of crashes
		'''
		results = "../tmp/pathfinder/"+self.binary+"/crashes/"
		cmd = "ls -1 "+results+" | wc -l "
		return cmd
