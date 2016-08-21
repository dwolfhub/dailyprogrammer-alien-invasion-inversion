#!/usr/bin/env python

import sys
import getopt


class Opening(object):
	def __init__(self, opening_indices):
		self.indices = opening_indices
	
	def __repr__(self):
		return str(self.indices)

	def matches_opening(self, opening):
		matching_indices = []
		for index in opening.indices:
			if index in self.indices:
				matching_indices.append(index)
		
		if len(matching_indices):
			return Opening(matching_indices)
		
		return False


class DashOpeningParser(object):
	def __init__(self):
		self.opening_char = '-'
	
	def get_openings(self, row):
		openings = []
		opening_indices = []
		for i, char in enumerate(row):
			if char == self.opening_char:
				opening_indices.append(i)
			elif len(opening_indices):
				openings.append(Opening(opening_indices))
				opening_indices = []
		
		if len(opening_indices):
			openings.append(Opening(opening_indices))

		return openings


class FieldParser(object):
	def __init__(self, ifile):
		assert isinstance(ifile, file)
		self.ifile = ifile
		self.squares = []
	
	def build_squares(self, openings):
		for square in self.squares:
			if square.rows == len(square.indices):
				pass
			elif square.opening.matches_opening:
				pass
			
	
	def get_biggest_square(self):
		for line in self.ifile:
			# remove newline char
			line = line[:-1]
			openings = find_openings(line)
			self.build_squares(openings)


def main(argv):
	input_file = ''

	try:
		opts, args = getopt.getopt(
			argv,
			'hi:',
			['ifile=']
		)
	except getopt.GetoptError:
		print 'aliens -i <inputfile>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'aliens -i <inputfile>'
		elif opt in ('-i', 'ifile'):
			input_file = arg
	
	with open(input_file, 'r') as ifile:
		# skip line 1
		next(ifile)

		print "Biggest square:"
		parser = FieldParser(ifile)
		print parser.get_biggest_square()


if __name__ == "__main__":
	main(sys.argv[1:])
