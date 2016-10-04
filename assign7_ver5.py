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
        self.parent=None


    def insert(self, val):
        if self.value:

            if val < self.value:
                if self.left is None:
                    self.left = node()
                    self.left.value=val
                    self.left.parent=self
                    parent = self.value
                    childl = self.left.value
                    edge = pydot.Edge(parent, childl)
                    # graph.add_edge(edge)
                    # print('Added Node Value To Left->'+str(self.left.value)+'Parent-->'+str(self.value))
                else:
                    self.left.insert(val)

            elif val > self.value:
                if self.right is None:
                    self.right = node()
                    self.right.value=val
                    self.right.parent = self
                    parent = self.value
                    childr = self.right.value
                    edge = pydot.Edge(parent, childr)
                    # graph.add_edge(edge)

                    # print('Added Node Value to Right->' + str(self.right.value) + 'Parent-->' + str(self.value))
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
    if Node.left==None and Node.right!=None:
        add_terminal(Node.right)
    elif Node.left!=None and Node.right==None:
        add_terminal(Node.left)
    elif Node.left != None and Node.right != None:
        add_terminal(Node.left)
        add_terminal(Node.right)
    else:
        Node.left=node()
        counter=counter+1
        Node.left.value=counter
        Node.left.key='Ter'
        parent = Node.value
        childl = Node.left.value

        edge = pydot.Edge(parent, childl)

        # graph.add_edge(edge)
        Node.right=node()
        Node.right.key = 'Ter'
        counter=counter+1
        Node.right.value = counter
        parent = Node.value
        childr = Node.right.value
        edge = pydot.Edge(parent, childr)
        # graph.add_edge(edge)


def add_edges(Node):
    if Node.left:
        edge = pydot.Edge(Node.value, Node.left.value)
        graph.add_edge(edge)
        add_edges(Node.left)
    if Node.right:
        edge = pydot.Edge(Node.value, Node.right.value)
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
    leng=int(len(yearlist))
    if leng>0:
        x = 1 << (leng.bit_length() - 1)
        if (x // 2 - 1) <= (leng - x):
            mid = x - 1
        else:
            mid = leng - x // 2
        # print('Value of Mid-->'+str(mid))
        if len(yearlist)==1:

            insert_element(yearlist[0])
        elif len(yearlist)>1:
            llist=yearlist[:mid]
            rlist=yearlist[mid+1:]

            insert_element(yearlist[mid])
            construct_stree(llist)
            construct_stree(rlist)




TREE=node()
graph = pydot.Dot(graph_type='graph')
intervalgraph = pydot.Dot(graph_type='graph')
counter=0

def interval_graph(filename):
    start_year=[]
    end_year=[]
    composer=[]
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
    length=len(start_year)
    for i in range(0,length):
        for j in range(i,length):
            if (start_year[i]<start_year[j]) and (end_year[i]>start_year[j]):
                edge = pydot.Edge(composer[i],composer[j])
                intervalgraph.add_edge(edge)
            elif (start_year[i]>start_year[j]) and (start_year[i]<end_year[j]):
                edge = pydot.Edge(composer[i],composer[j])
                intervalgraph.add_edge(edge)
    filename = 'interval_graph' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png'
    intervalgraph.write_png(filename)

def main():
    # print_csv('sample-data.csv')

    yearlist = parse_year('sample-data.csv')
    # print(yearlist)
    # construct_stree(yearlist)
    # add_terminal(TREE)
    # print_graph()
    interval_graph('sample-data.csv')



if __name__ == '__main__': main()
