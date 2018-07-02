''' Implement your driver for your own fuzzer here.	By convention it must write its 
	outputs (which are expected to be inputs to the target program) to results/<fuzzername>/<projectname>/<binaryname>/queue. 
	Easiest way to start is the class of another fuzzer and modify it.
'''

class AFL():
	''' default afl installation (tested with 2.52b)
	'''

	def __init__(self):
		self.name = "afl"
		# set this to true if you have custom compiled binaries (this will expect build binaries as subfolder like projects/afl/ instead of just in projects/)
		self.custom = False

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


class LAF():
	''' https://lafintel.wordpress.com/, we force this into -Q mode since this is binary comparison and we dont want to cheat
	'''

	def __init__(self):		
		self.name = "laf"		
		self.custom = True

	def pre(self, project, binary, args):
		''' Prepare environment and run the fuzzer
		'''
		self.project = project
		self.binary = binary
		self.args = args
		results = "results/"+self.name+"/"+self.project+"/"+self.binary
		cmd = "mkdir -p "+results+" && "
		# callee location modified for subfolder
		cmd += "AFL_SKIP_BIN_CHECK=1 ../laf/afl-fuzz -i seeds/ -o "+results+" -Q -m none targets/"+ self.name + "/" +self.project+"/"+self.binary+" "+''.join(self.args)
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
	''' pathfinder in normal mode
	'''
	
	def __init__(self):		
		self.name = "pathfinder"
		self.custom = False

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


class PathfinderHybrid():
	''' this is just copy pasted from pathfinder with an added -hybrid flag
	'''
	
	def __init__(self):		
		self.name = "pathfinder_hybrid"
		self.custom = False

	def pre(self, project, binary, args):
		''' Prepare environment and run the fuzzer
		'''
		self.project = project
		self.binary = binary
		self.args = args
		cmd = "cd ../pathfinder/ && "
		cmd += "python fuzzer.py -hybrid -i ../fuzz-perf/seeds/ "
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

