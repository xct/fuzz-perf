''' Implement your driver for your own fuzzer here.	By convention it must write its 
	outputs (which are expected to be inputs to the target program) to results/<name>/files. 
	Easiest way to start is the class of another fuzzer and modify it.
'''

class AFL():

	def __init__(self):		
		self.name = "AFL"

	def pre(self, project, binary, args):
		return "pwd"

	def post(self):
		return "pwd"


class PathfinderDriver():
	
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
		cmd = "mkdir -p results/"+self.project+"/"+self.binary+"/queue/"
		cmd += "; rm results/"+self.project+"/"+self.binary+"/*"
		cmd += "; rm results/"+self.project+"/"+self.binary+"/queue/*"
		cmd += "; cp ../tmp/pathfinder/"+self.binary+"/queue/* results/"+self.project+"/"+self.binary+"/queue/"
		print(cmd)
		return cmd
