#This version only prints output from csv file to terminal
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

def print_year(filename):


    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            print(row[2])


def main():
    print_csv('sample-data.csv')
    print_year('sample-data.csv')

if __name__ == '__main__':main()
