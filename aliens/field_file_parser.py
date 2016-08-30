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

class Square(object):
    """
    squares have an opening and a number of rows
    """
    def __init__(self, opening):
        self.rows = 1
        self.opening = opening

    def size(self):
        """
        the size of a square is the lower of rows or indices length squared
        """
        square_size = self.rows**2
        openings_len = len(self.opening.indices) 
        if openings_len < self.rows:
            square_size = openings_len**2

        return square_size


class FieldParser(object):
    def __init__(self, ifile, parser):
        self.ifile = ifile
        self.squares = []
        self.parser = parser
        self.biggest_square = None

    def build_squares(self, openings):
        new_squares = []
        for opening in openings:
            # see if opening continues a square
            square_continued = False

            for square in self.squares:
                new_opening = square.opening.matches_opening(opening)
                if new_opening:
                    square.rows += 1

                    if square.size() > self.biggest_square: 
                        # record new biggest square
                        self.biggest_square = square.size()
                    
                    square.opening = new_opening 
                    new_squares.append(square)
                    if len(square.opening.indices) == len(opening.indices):
                        square_continued = True

            # new square
            if not square_continued:
                new_squares.append(Square(opening))

        self.squares = new_squares
            
    def get_biggest_square(self):
        for line in self.ifile:
            # remove newline char
            line = line[:-1]
            openings = self.parser.get_openings(line)
            if len(openings):
                self.build_squares(openings)

        return self.biggest_square


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
        parser = FieldParser(ifile, DashOpeningParser)
        print parser.get_biggest_square()


if __name__ == "__main__":
    main(sys.argv[1:])
