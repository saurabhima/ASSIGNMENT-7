import csv

csv.register_dialect(
    'mydialect',
    delimiter=',',
    quotechar='"',
    doublequote=True,
    skipinitialspace=True,
    lineterminator='\r\n',
    quoting=csv.QUOTE_MINIMAL)


def print_csv(filename):
    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            length = len(row)
            for i in range(0, length):
                print(row[i] + "\t \t", end='')
            print('\n')


def parse_year(filename):
    yearlist=[]
    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            year=row[2]
            loc=year.find('-')
            if loc>0:
                year1=year[:loc]
                year2=year[loc+1:]
                yearlist.append(year1)
                yearlist.append(year2)
    yearlist.sort()
    return yearlist



class node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val

class interval_tree:
    def __init__(self):
        self.root=None

def main():
    # print_csv('sample-data.csv')
    yearlist=[]
    yearlist=parse_year('sample-data.csv')
    print(yearlist)


if __name__ == '__main__': main()
