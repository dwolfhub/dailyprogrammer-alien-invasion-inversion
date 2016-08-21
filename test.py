import unittest
from aliens import field_file_parser

class TestOpening(unittest.TestCase):

	def test_opening_sets_indices(self):
		opening = field_file_parser.Opening([0,1,2])
		self.assertEqual([0,1,2], opening.indices)
	
	def test_matches_opening(self):
		opening_1 = field_file_parser.Opening([0,1,2])
		opening_2 = field_file_parser.Opening([0,1])
		match = opening_1.matches_opening(opening_2)
		self.assertEquals([0,1], match.indices)

class TestDashOpeningParser(unittest.TestCase):
	
	def test_init_sets_opening_char(self):
		parser = field_file_parser.DashOpeningParser()
		self.assertEqual('-', parser.opening_char)

	def test_get_openings_returns_array_of_openings(self):
		parser = field_file_parser.DashOpeningParser()
		openings = parser.get_openings('---x--x----')
		self.assertEquals(3, len(openings))
		self.assertEqual([0,1,2], openings[0].indices)
		self.assertEqual([4,5], openings[1].indices)
		self.assertEqual([7,8,9,10], openings[2].indices)

		openings = parser.get_openings('')



		

if __name__ == '__main__':
	unittest.main()
