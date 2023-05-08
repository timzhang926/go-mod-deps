import argparse
import os
import sys
from queue import Queue
import json
import pydot

# Add go mod graph file to graph
def add_to_graph(graph, line):
    x = line.strip().split(" ")
    if len(x) < 2:
        return
    # dependencies
    if x[0] not in graph:
        graph[x[0]] = {}
    if "dependencies" not in graph[x[0]]:
        graph[x[0]]["dependencies"] = []
    graph[x[0]]["dependencies"].append(x[1])
    # remove duplicate
    # graph[x[0]]["dependencies"] = list(set(graph[x[0]]["dependencies"]))

    # dependents
    if x[1] not in graph:
        graph[x[1]] = {}
    if "dependents" not in graph[x[1]]:
        graph[x[1]]["dependents"] = []
    graph[x[1]]["dependents"].append(x[0])


def print_graph_flat(graph):
    root_symbol1 = ""
    root_symbol2 = ""
    child_symbol1 = ""
    child_symbol2 = ""
    for x in graph:
        if x != list(graph)[-1]:
            root_symbol1 = "├─ "
            root_symbol2 = "│  "
        else:  # Last one
            root_symbol1 = "└─ "
            root_symbol2 = "   "
        print(root_symbol1 + x)

        if "dependencies" in graph[x]:
            child_symbol1 = "├─ "
            child_symbol2 = "│  "
        else:  # Last one
            child_symbol1 = "└─ "
            child_symbol2 = "   "

        if "dependents" in graph[x]:
            print(root_symbol2 + child_symbol1 + "dependents")
            for i in range(len(graph[x]["dependents"]) - 1):
                print(root_symbol2 + child_symbol2 + "├─ " + graph[x]["dependents"][i])
            print(root_symbol2 + child_symbol2 + "└─ " + graph[x]["dependents"][len(graph[x]["dependents"]) - 1])
            if "dependencies" in graph[x]:
                print(root_symbol2 + child_symbol2)

        if "dependencies" in graph[x]:
            print(root_symbol2 + "└─ dependencies")
            for i in range(len(graph[x]["dependencies"]) - 1):
                print(root_symbol2 + "   " + "├─ " + graph[x]["dependencies"][i])
            print(root_symbol2 + "   " + "└─ " + graph[x]["dependencies"][len(graph[x]["dependencies"]) - 1])
        print(root_symbol2)


def add_to_dotgraph(dg, line):
    x = line.strip().split(" ")
    if len(x) < 2:
        return
    dg.add_edge(pydot.Edge(x[0], x[1]))


def bfs(node, graph, dotgraph):
    vSet = set()  # visited nodes set
    if node is None:
        return
    queue = Queue()
    nodeSet = set()
    queue.put(node)
    nodeSet.add(node)
    while not queue.empty():
        cur = queue.get()  # Get one element
        vSet.add(cur)
        if "dependents" not in graph[cur]:  # Continue if cur has no dependents
            continue
        for next in graph[cur]["dependents"]:  # Visit its adjacent nodes
            add_to_dotgraph(dotgraph, next + " " + cur)
            if next not in nodeSet:  # If the adjacent nodes are not in queue the add it
                nodeSet.add(next)
                queue.put(next)
    return vSet


# Python program to illustrate the intersection
# of two lists in most simple way
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def create_subgraph(graph, vset):
    subgraph = {}
    for x in graph:
        if x not in vset:
            continue
        subgraph[x] = {}
        if "dependents" in graph[x]:
            for d in graph[x]["dependents"]:
                if d not in vset:
                    continue
                if "dependents" not in subgraph[x]:
                    subgraph[x]["dependents"] = []
                subgraph[x]["dependents"].append(d)
        elif "dependencies" in graph[x]:
            for d in graph[x]["dependencies"]:
                if d not in vset:
                    continue
                if "dependencies" not in subgraph[x]:
                    subgraph[x]["dependencies"] = []
                subgraph[x]["dependencies"].append(d)
    return subgraph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='gomoddeps',
        description='Convert <go mod graph> output to a flat dependency tree, json, dot, png, svg file, and find all dependency paths to the input package.',
        epilog='See <https://github.com/zhangxd926/go-mod-deps> for the full manual.')

    parser.add_argument('packagename', nargs='?',
                        help="the package you want to search, it must exists in <go mod graph> output")  # positional argument
    parser.add_argument('-i', '--inputfile',
                        help="the file that created by <go mod graph> command")  # option that takes a value
    parser.add_argument('-t', '--type', choices=['txt', 'json', 'dot', 'png', 'svg'],
                        help="output file type")  # option that takes a value
    parser.add_argument('-o', '--outputfile')  # option that takes a value
    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    args = parser.parse_args()
    if args.verbose:
        print("packagename:", args.packagename, "inputfile:", args.inputfile, "filetype:", args.type, "outputfile:",
              args.outputfile, "verbose:",
              args.verbose)

    gGraph = {}
    dotgraph = pydot.Dot('gomodgraph', graph_type='digraph', bgcolor='azure')
    dotgraph.set_node_defaults(shape="box", style="rounded")
    if args.inputfile is not None:
        if os.path.isfile(args.inputfile):
            if args.verbose:
                print("Reading file:", args.inputfile)
            with open(args.inputfile) as fp:
                Lines = fp.readlines()
                for line in Lines:
                    add_to_graph(gGraph, line)
                    add_to_dotgraph(dotgraph, line)
        else:
            sys.stderr.write(args.inputfile + " doesn't exist!\n")
    else:  # read stdin
        for line in sys.stdin:
            # print(line.strip())
            if 'q' == line.rstrip():
                break
            add_to_graph(gGraph, line)
            add_to_dotgraph(dotgraph, line)
    if args.verbose:
        print("Graph length:", len(gGraph))

    # No package provided
    if args.packagename is None:
        if args.type == "json":
            json_object = json.dumps(gGraph,
                                     default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value),
                                     indent=4, allow_nan=False)
            if args.outputfile is None:
                print(json_object)
            else:
                with open(args.outputfile, 'w') as sys.stdout:
                    print(json_object)
        elif args.type == "dot":
            if args.outputfile is None:
                print(dotgraph.to_string())
            else:
                with open(args.outputfile, 'w') as sys.stdout:
                    print(dotgraph.to_string())
        elif args.type == "png":
            if args.outputfile is None:
                sys.stderr.write("Please provide the png output file name!\n")
            else:
                print("Creating png file ...")
                dotgraph.write_png(args.outputfile)
                print("Done!")
        elif args.type == "svg":
            if args.outputfile is None:
                sys.stderr.write("Please provide the svg output file name!\n")
            else:
                print("Creating svg file ...")
                dotgraph.write_svg(args.outputfile)
                print("Done!")
        else:
            if args.outputfile is None:
                print_graph_flat(gGraph)
            else:
                with open(args.outputfile, 'w') as sys.stdout:
                    print_graph_flat(gGraph)
    else:
        if args.packagename not in gGraph:
            sys.stderr.write(args.packagename + " doesn't exist!\n")
        else:
            dotgraph2 = pydot.Dot('gomodgraph_subset', graph_type='digraph', bgcolor='azure')
            dotgraph2.set_node_defaults(shape="box", style="rounded")
            gSet = bfs(args.packagename, gGraph, dotgraph2)
            subgraph = create_subgraph(gGraph, gSet)
            if args.verbose:
                print("Number of nodes that access the input package:", len(gSet))

            if args.type == "json":
                json_object = json.dumps(subgraph,
                                         default=lambda o: dict(
                                             (key, value) for key, value in o.__dict__.items() if value),
                                         indent=4, allow_nan=False)
                if args.outputfile is None:
                    print(json_object)
                else:
                    with open(args.outputfile, 'w') as sys.stdout:
                        print(json_object)
            elif args.type == "dot":
                if args.outputfile is None:
                    print(dotgraph2.to_string())
                else:
                    with open(args.outputfile, 'w') as sys.stdout:
                        print(dotgraph2.to_string())
            elif args.type == "png":
                if args.outputfile is None:
                    sys.stderr.write("Please provide the png output file name!\n")
                else:
                    print("Creating png file ...")
                    dotgraph2.write_png(args.outputfile)
                    print("Done!")
            elif args.type == "svg":
                if args.outputfile is None:
                    sys.stderr.write("Please provide the svg output file name!\n")
                else:
                    print("Creating svg file ...")
                    dotgraph2.write_svg(args.outputfile)
                    print("Done!")
            else:
                if args.outputfile is None:
                    print_graph_flat(subgraph)
                else:
                    with open(args.outputfile, 'w') as sys.stdout:
                        print_graph_flat(subgraph)
