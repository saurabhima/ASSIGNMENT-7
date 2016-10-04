import csv

import datetime
import graphviz
import pydot
import random

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
    yearlist = []

    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            year = row[2]
            loc = year.find('-')
            if loc > 0:
                year1 = year[:loc]
                year2 = year[loc + 1:]
                yearlist.append(int(year1))
                yearlist.append(int(year2))
    yearlist.sort()
    return yearlist


class node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None
        self.key = None
        self.parent = None
        self.begin = None
        self.end = None
        self.composer = []

    def insert(self, val):
        if self.value:

            if val < self.value:
                if self.left is None:
                    self.left = node()
                    self.left.value = val
                    self.left.parent = self

                else:
                    self.left.insert(val)

            elif val > self.value:
                if self.right is None:
                    self.right = node()
                    self.right.value = val
                    self.right.parent = self
                else:
                    self.right.insert(val)

        else:
            self.value = val

            # print('Root being Created with Value' + str(self.value))

    def create_graph(self):
        filename = 'data_graph' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png'
        graph.write_png(filename)

    def return_root(self):
        return str(TREE.value)


def add_terminal(Node):
    global counter
    if Node.left == None and Node.right != None:
        Node.left = node()
        counter = counter + 1
        Node.left.value = counter
        Node.left.key = 'Ter'
        Node.left.left = None
        Node.left.right = None
        Node.left.parent = Node
        add_terminal(Node.right)
    elif Node.left != None and Node.right == None:
        Node.right = node()
        Node.right.key = 'Ter'
        counter = counter + 1
        Node.right.value = counter
        Node.right.left = None
        Node.right.right = None
        Node.right.parent = Node
        add_terminal(Node.left)
    elif Node.left != None and Node.right != None:
        add_terminal(Node.left)
        add_terminal(Node.right)
    else:
        Node.left = node()
        counter = counter + 1
        Node.left.value = counter
        Node.left.key = 'Ter'
        Node.left.left = None
        Node.left.right = None
        Node.left.parent = Node

        Node.right = node()
        Node.right.key = 'Ter'
        counter = counter + 1
        Node.right.value = counter
        Node.right.left = None
        Node.right.right = None
        Node.right.parent = Node


def add_edges(Node):
    global node_count

    if Node.parent == None:

        labelstr = '{<f0>' + str(Node.value) + '|{<f1>' + str(Node.begin) + '|<f2>' + str(Node.end) + '}}'
        if Node.key == 'Ter':
            labelstr = labelstr + '|<f3>' + str(Node.key)

        if len(Node.composer) > 0:
            labelstr = labelstr + '|<f4>' + str(Node.composer)
        node_a = pydot.Node(Node.value, label=labelstr, shape="record", fillcolor="red")
        graph.add_node(node_a)
    if Node.left:

        labelstr = '{<f0>' + str(Node.left.value) + '|{<f1>' + str(Node.left.begin) + '|<f2>' + str(
            Node.left.end) + '}}'
        if Node.left.key == 'Ter':
            labelstr = labelstr + '|<f3>' + str(Node.left.key)

        if len(Node.left.composer) > 0:
            labelstr = labelstr + '|<f4>' + str(Node.left.composer)

        node_b = pydot.Node(Node.left.value, label=labelstr, shape="record", fillcolor="red")

        graph.add_node(node_b)
        edge = pydot.Edge(Node.value, node_b)
        graph.add_edge(edge)
        add_edges(Node.left)
    if Node.right:

        labelstr = '{<f0>' + str(Node.right.value) + '|{<f1>' + str(Node.right.begin) + '|<f2>' + str(
            Node.right.end) + '}}'
        if Node.right.key == 'Ter':
            labelstr = labelstr + '|<f3>' + str(Node.right.key)

        if len(Node.right.composer) > 0:
            labelstr = labelstr + '|<f4>' + str(Node.right.composer)
        node_c = pydot.Node(Node.right.value, label=labelstr, shape="record", fillcolor="red")

        graph.add_node(node_c)
        edge = pydot.Edge(Node.value, node_c)
        graph.add_edge(edge)
        add_edges(Node.right)


def print_graph():
    add_edges(TREE)

    filename = 'data_graph' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png'
    graph.write_png(filename)


def insert_element(year):
    TREE.insert(year)


def print_list(yearlist):
    print(yearlist)


def construct_stree(yearlist):
    # print('Total Elements-->'+str(len(yearlist)))
    leng = int(len(yearlist))
    if leng > 0:
        x = 1 << (leng.bit_length() - 1)
        if (x // 2 - 1) <= (leng - x):
            mid = x - 1
        else:
            mid = leng - x // 2
        # print('Value of Mid-->'+str(mid))
        if len(yearlist) == 1:

            insert_element(yearlist[0])
        elif len(yearlist) > 1:
            llist = yearlist[:mid]
            rlist = yearlist[mid + 1:]

            insert_element(yearlist[mid])
            construct_stree(llist)
            construct_stree(rlist)


def insert_intervals(Node):
    if Node.parent == None:
        Node.begin = -10000
        Node.end = 9999999

    elif Node == Node.parent.left:
        Node.begin = Node.parent.begin
        Node.end = Node.parent.value

        # print('Added Interval for Node ' + str(Node.value) + ' Parent -' + str(Node.parent.value) + ' Begin - ' + str(
        #     Node.begin) + ' End - ' + str(Node.end))
    elif Node == Node.parent.right:
        Node.begin = Node.parent.value
        Node.end = Node.parent.end

        # print('Added Interval for Node ' + str(Node.value) + ' Parent -' + str(Node.parent.value) + ' Begin - ' + str(
        #     Node.begin) + ' End - ' + str(Node.end))
    if Node.left:
        insert_intervals(Node.left)
    if Node.right:
        insert_intervals(Node.right)


TREE = node()
graph_nodes = []
node_count = 0
graph = pydot.Dot(graph_type='graph')
intervalgraph = pydot.Dot(graph_type='graph')
counter = 0
overlap_list = []
max_overlap_list = []
max_overlap_startyear = []
max_overlap_endyear = []


def interval_graph(filename):
    start_year = []
    end_year = []
    composer = []
    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            year = row[2]
            loc = year.find('-')
            if loc > 0:
                year1 = year[:loc]
                year2 = year[loc + 1:]
                start_year.append(int(year1))
                end_year.append(int(year2))
                composer.append(row[1])
    length = len(start_year)
    for i in range(0, length):
        for j in range(i, length):
            if (start_year[i] < start_year[j]) and (end_year[i] > start_year[j]):
                edge = pydot.Edge(composer[i], composer[j])
                intervalgraph.add_edge(edge)
            elif (start_year[i] > start_year[j]) and (start_year[i] < end_year[j]):
                edge = pydot.Edge(composer[i], composer[j])
                intervalgraph.add_edge(edge)
    filename = 'interval_graph' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png'
    intervalgraph.write_png(filename)


def add_span_sub(Node, start_year, end_year, composer):
    if Node.begin >= start_year and Node.end <= end_year and (
                    Node.parent.begin < start_year or Node.parent.end > end_year):
        # print('Added Composer '+composer +'to Node '+str(Node.value))
        Node.composer.append(composer)
    if Node.left:
        add_span_sub(Node.left, start_year, end_year, composer)
    if Node.right:
        add_span_sub(Node.right, start_year, end_year, composer)


def add_span(Node, filename):
    start_year = []
    end_year = []
    composer = []
    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:
            year = row[2]
            loc = year.find('-')
            if loc > 0:
                year1 = year[:loc]
                year2 = year[loc + 1:]
                start_year.append(int(year1))
                end_year.append(int(year2))
                composer.append(row[1])
    for row in range(0, len(start_year)):
        add_span_sub(Node, start_year[row], end_year[row], composer[row])


def insert_composer(Node, composer_name, year_block):
    loc = year_block.find('-')
    if loc > 0:
        startyear = int(year_block[:loc])
        endyear = int(year_block[loc + 1:])
        add_span_sub(Node, startyear, endyear, composer_name)


def find_overlap(Node, startyear, endyear):
    overlap = False
    global overlap_list
    if Node.begin <= startyear and Node.end >= startyear:
        overlap = True
    if Node.begin >= startyear and Node.begin <= endyear:
        overlap = True
    if overlap == True:

        if len(Node.composer) > 0:
            for rg in range(0, len(Node.composer)):
                if Node.composer[rg] not in overlap_list:
                    overlap_list.append(Node.composer[rg])
                    # print('Overlap Found With -->'+str(Node.composer))

    if Node.left:
        find_overlap(Node.left, startyear, endyear)
    if Node.right:
        find_overlap(Node.right, startyear, endyear)


def find_max_overlap(Node, startyear, endyear):
    overlap = False
    global max_overlap_list, max_overlap_startyear, max_overlap_endyear
    if Node.begin <= startyear and Node.end >= startyear:
        overlap = True
    if Node.begin >= startyear and Node.begin <= endyear:
        overlap = True
    if overlap == True:

        if len(Node.composer) > 0:
            for rg in range(0, len(Node.composer)):
                if Node.composer[rg] not in max_overlap_list:
                    max_overlap_list.append(Node.composer[rg])

                    print('Overlap Found With -->'+str(Node.composer))

    if Node.left:
        find_max_overlap(Node.left, startyear, endyear)
    if Node.right:
        find_max_overlap(Node.right, startyear, endyear)
def check_max_overlap(filename):
    global max_overlap_list, max_overlap_startyear, max_overlap_endyear
    yearlist = []
    composer1=''
    composer2=''
    interval_start=0
    interval_end=0
    max_overlap=0
    print(max_overlap_list)
    with open(filename, 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')

        for row in thedata:

            year = row[2]
            loc = year.find('-')
            if loc > 0:
                if row[1] in max_overlap_list:
                    startyear = int(year[:loc])
                    endyear = int(year[loc + 1:])
                    max_overlap_startyear.append(startyear)
                    max_overlap_endyear.append(endyear)

    for i in range(0,len(max_overlap_list)):
        for j in range(i+1,len(max_overlap_list)):
            if max_overlap_startyear[i]<max_overlap_startyear[j] and max_overlap_endyear[i]>max_overlap_endyear[j]:
                overlap=max_overlap_endyear[j]-max_overlap_startyear[j]

            elif max_overlap_startyear[i]>max_overlap_startyear[j] and max_overlap_endyear[i]<max_overlap_endyear[j]:
                overlap=max_overlap_endyear[i]-max_overlap_startyear[i]
            elif max_overlap_startyear[i]<max_overlap_startyear[j] and max_overlap_endyear[i]<max_overlap_endyear[j]:
                overlap=max_overlap_endyear[i]-max_overlap_startyear[j]
            elif max_overlap_startyear[i]>max_overlap_startyear[j] and max_overlap_endyear[i]>max_overlap_endyear[j]:
                overlap=max_overlap_endyear[j]-max_overlap_startyear[i]


            if overlap > max_overlap:
                max_overlap = overlap
                composer1 = max_overlap_list[i]
                composer2 = max_overlap_list[j]
    print('Max Overlap->'+str(max_overlap))
    print('Composer 1-->'+composer1)
    print('Composer 2-->' + composer2)

def main():
    print("Assignment 7 Interval Tree Implementation")
    while (True):

        print("1>Built Interval Tree")
        print("2> Insert Composer")
        print("3> Print Tree")
        print("4> Find Overlaps")
        print("5> Max Overlap")
        print("6> Find Songs")
        print("7> Build Interval Graph")
        # print("8> Remove Max")
        # print("9> Remove Min")
        #
        # print("10> Print PQ")
        print("0> Exit")
        user_input = int(input("Please Select an Option-->"))
        if user_input == 1:
            file_input = input("Please Enter filename-->")
            yearlist = parse_year(file_input)
            # print(yearlist)
            construct_stree(yearlist)
            add_terminal(TREE)
            insert_intervals(TREE)
            add_span(TREE, file_input)
        elif user_input == 2:
            composer_name = input("Please Enter Composer Name-->")
            composer_period = input("Please Enter Composer Period-->")
            insert_composer(TREE, composer_name, composer_period)
        elif user_input == 3:
            print_graph()
        elif user_input == 4:
            check_period = input("Please Enter Period to Check-->")
            loc = check_period.find('-')
            if loc > 0:
                startyear = int(check_period[:loc])
                endyear = int(check_period[loc + 1:])
                find_overlap(TREE, startyear, endyear)
                overlap_list.sort()
                print(overlap_list)
        elif user_input == 5:
            check_period = input("Please Enter Period to Check-->")
            loc = check_period.find('-')
            if loc > 0:
                startyear = int(check_period[:loc])
                endyear = int(check_period[loc + 1:])
                find_max_overlap(TREE, startyear, endyear)
                check_max_overlap(file_input)

        elif user_input == 6:
            print('OPtion 6')
        elif user_input == 7:
            interval_graph(file_input)
        # elif user_input == 8:
        #     maxout = MAX_HEAP.RemoveMax()
        #     print(maxout)
        #     MIN_HEAP.Remove(maxout)
        # elif user_input == 9:
        #     minout = MIN_HEAP.RemoveMin()
        #     print(minout)
        #     MAX_HEAP.Remove(minout)
        #
        # elif user_input == 10:
        #     MIN_HEAP.print_MIN_HEAP()
        #     MAX_HEAP.print_MAX_HEAP()
        else:
            return 0

    print_graph()
    # interval_graph('sample-data.csv')


if __name__ == '__main__': main()
