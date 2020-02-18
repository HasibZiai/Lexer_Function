#!/usr/bin/python


# Open the file
with open("data.txt", "r") as fileHandler:
	# Read next line
	line = fileHandler.readline()
	# check if line is not empty
	while line:
		print(line.strip())
		line = fileHandler.readline()
