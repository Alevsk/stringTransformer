#!/usr/bin/env python

"""
Copyright (c) 2016 Lenin Alevski Huerta Arias.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function

import re
import imp
import os
import sys

from subprocess import Popen, PIPE
from time import strftime
from optparse import OptionParser
from random import sample
from os import listdir, makedirs
from os.path import isfile, join, dirname, exists

from lib.common import color
from lib.settings import BW
from lib.settings import ASK, PLUS, INFO, TEST, WARN, ERROR, DEBUG
from lib.logger import logger

sys.dont_write_bytecode = True

NAME = "stringTransformer"
VERSION = "v0.1"
URL = "https://github.com/alevsk/stringTransformer/"

# Maximum length of left option column in help listing
MAX_HELP_OPTION_LENGTH = 20

BANNER = """                  
              _______         
       _____ |   _   |  ____  
      |    |  \  V  /  |    | 
      |   \ \  \_ _/  / /   | 
      \  \ \ \   '   / / /  / 
       \  \   | 'V' |   /  /  
     |\ \_____| \ / |_____/ /|
     | \        | |        / |
     |  |    ,/|| ||\,    |  |
     |   `| '  || ||  ' |`   |
     |    | |  || ||  | |    |
     \    | |  || ||  | |    /
      \.  | |  ||_||  | |  ./ 
       \  | |  |___|  | |  /  
         \\' ,  _____  , '/    
             \/ ___ \/        
               /___\          
                           """

REPRESENTATIONS_DIR = "representations"

# Location of the folder where results will be written to
OUTPUT_DIR = "output"

# Location of Git repository
GIT_REPOSITORY = "https://github.com/alevsk/stringTransformer.git"

EXAMPLES = """
Examples:
./stringTransformer.py -i [STRING]
./stringTransformer.py -i [STRING] --exclude "hexa, octal"
./stringTransformer.py -i [STRING] --only "hexa, octal"
./stringTransformer.py -i [STRING] --params "rot.cipher=13,rot.encoding=utf-8"
./stringTransformer.py --load list.txt
./stringTransformer.py --list
"""

def print(*args, **kwargs):
	"""
	Currently no purpose.
	"""

	return __builtins__.print(*args, **kwargs)

def update():
	"""
	Updates the program via git pull.
	"""

	print("%s Checking for updates..." % INFO)

	process = Popen("git pull %s HEAD" % GIT_REPOSITORY, shell=True,
					stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	success = not process.returncode

	if success:
		updated = "Already" not in stdout
		process = Popen("git rev-parse --verify HEAD", shell=True,
						stdout=PIPE, stderr=PIPE)
		stdout, _ = process.communicate()
		revision = (stdout[:7] if stdout and
					re.search(r"(?i)[0-9a-f]{32}", stdout) else "-")
		print("%s the latest revision '%s'." %
			  ("%s Already at" % INFO if not updated else
			   "%s Updated to" % PLUS, revision))
	else:
		print("%s Problem occurred while updating program.\n" % WARN)

		_ = re.search(r"(?P<error>error:[^:]*files\swould\sbe\soverwritten"
					  r"\sby\smerge:(?:\n\t[^\n]+)*)", stderr)
		if _:
			def question():
				"""Asks question until a valid answer of y or n is provided."""
				print("\n%s Would you like to overwrite your changes and set "
					  "your local copy to the latest commit?" % ASK)
				sys_stdout.write("%s ALL of your local changes will be deleted"
								 " [Y/n]: " % WARN)
				_ = raw_input()

				if not _:
					_ = "y"

				if _.lower() == "n":
					exit()
				elif _.lower() == "y":
					return
				else:
					print("%s Did not understand your answer! Try again." %
						  ERROR)
					question()

			print("%s" % _.group("error"))

			question()

			if "untracked" in stderr:
				cmd = "git clean -df"
			else:
				cmd = "git reset --hard"

			process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
			stdout, _ = process.communicate()

			if "HEAD is now at" in stdout:
				print("\n%s Local copy reset to current git branch." % INFO)
				print("%s Attemping to run update again..." % INFO)
			else:
				print("%s Unable to reset local copy to current git branch." %
					  WARN)
				exit()

			update()
		else:
			print("%s Please make sure that you have "
				  "a 'git' package installed." % INFO)
			print(stderr)

def list_representations(extension=False):
	"""
	List available string representations for input transformation found in the representations folder.
	"""
	return [_ if extension else _.replace(".py", "")
			for _ in listdir(REPRESENTATIONS_DIR) if isfile(join(REPRESENTATIONS_DIR, _))]

def load_representations(list):
	"""
	Load transformation modules dynamically
	"""
	modules = []
	for file in list:
		module = imp.load_source(file, "%s/%s.py" % (REPRESENTATIONS_DIR, file))
		if hasattr(module, file):
			rep = getattr(module, file)()
			modules.append(rep)
			
	return modules


def parseParams(params):
	parameters = {}
	params = params.split(',')
	
	for param in params:
		a = param.split('=')
		b = a[0].split('.')
		if b[0] in parameters:
			obj = parameters[b[0]]
			obj[b[1]] = a[1]
		else:
			obj = {}
			obj[b[1]] = a[1]
			parameters[b[0]] = obj

	return parameters

def parse_args():
	"""
	Parses the command line arguments.
	"""
	# Override epilog formatting
	OptionParser.format_epilog = lambda self, formatter: self.epilog

	parser = OptionParser(usage="usage: %prog -i INPUT_STRING | --input INPUT_STRING "
						  "| --load FILE",
						  epilog=EXAMPLES)

	parser.add_option("-i", "--input", dest="input",
					  help="set the input string to test with")

	parser.add_option("-l", "--load", dest="load_file",
					  help="load list of input strings (one per line)")

	parser.add_option("-x", "--exclude", dest="exclude",
					  help="exclude this representations")

	parser.add_option("-o", "--only", dest="only",
					  help="transform input only to this representations")

	parser.add_option("-O", "--output", dest="output",
					  help="generate an output file")

	parser.add_option("-p", "--params", dest="params",
					  help="use custom parameters on transformation functions")

	parser.add_option("--list", action="store_true", dest="list",
					  help="list available input representations")

	parser.add_option("--update", action="store_true", dest="update",
					  help="update from the official git repository")

	parser.formatter.store_option_strings(parser)
	parser.formatter.store_option_strings = lambda _: None

	for option, value in parser.formatter.option_strings.items():
		value = re.sub(r"\A(-\w+) (\w+), (--[\w-]+=(\2))\Z", r"\g<1>/\g<3>",
					   value)
		value = value.replace(", ", '/')
		if len(value) > MAX_HELP_OPTION_LENGTH:
			value = ("%%.%ds.." % (MAX_HELP_OPTION_LENGTH -
								   parser.formatter.indent_increment)) % value
		parser.formatter.option_strings[option] = value

	args = parser.parse_args()[0]

	if not any((args.input, args.update,
				args.list, args.load_file)):
		parser.error("Required argument is missing. Use '-h' for help.")

	return args

def main():
	"""
	Initializes and executes the program.
	"""

	print("%s\n\n%s %s (%s)\n" % (BANNER, NAME, VERSION, URL))

	args = parse_args()

	if args.update:
		update()
		exit()

	if args.list:
		representations = list_representations()
		for _ in representations:
			print("- %s" % _)
			
		print("\n")
		exit()

	inputs = []
	params = {}
	output = ""
	
	representations = list_representations()

	if args.only:
		representations = [representation for representation in representations if representation in args.only]
	elif args.exclude:
		representations = [representation for representation in representations if representation not in args.exclude]

	print("%s Loaded %d %s to apply." %
		(INFO, len(representations), "representations" if len(representations) == 1 else "representations"))

	if args.load_file:
		if not isfile(args.load_file):
			print("%s could not find the file \"%s\"" %
				  (WARN, color(args.load_file)))
			exit()

		_ = sum(1 for line in open(args.load_file, "r"))
		if _ < 1:
			print("%s the file \"%s\" doesn't contain any valid input." %
				  (WARN, color(args.load_file)))
			exit()

		inputs += [line.rstrip('\n') for line in open(args.load_file, "r")]

		print("%s Loaded %d input strings%s from \"%s\".\n" %
			  (INFO, _, "s" if _ != 1 else "", color(args.load_file)))

	if args.input:
		inputs.append(args.input)

	if(args.params):
		params = parseParams(args.params)

	print("%s Starting tests at: \"%s\"\n" % (INFO, color(strftime("%X"), BW)))

	if not exists(OUTPUT_DIR):
		makedirs(OUTPUT_DIR)

	modules = load_representations(representations)

	for string in inputs:
		print("%s\n\n%s applying transformation...\n" % (string, INFO))
		for module in modules:
			transformation = module.transform(string, params[module.__class__.__name__] if module.__class__.__name__ in params else {}) + "\n"
			output += transformation
			print(module.__class__.__name__ + ":\n")
			print(transformation)
		print("==================================\n")

	if args.output:
		f = open(OUTPUT_DIR + '/' + args.output,'w')
		f.write(output)
		f.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n%s Ctrl-C pressed." % INFO)