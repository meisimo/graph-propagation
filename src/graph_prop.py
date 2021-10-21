from matplotlib import pyplot as plt
import numpy as np

from typing import Any, Dict, List, Tuple

def csv_to_matrix(name:str) -> Tuple[List[str], List[List[int]]]:
    try:
        file = open('../data/input/' + name)
    except:
        print("Error loading " + name + " file")
        exit(1)

    try:
        M = [[cel.strip() for cel in row.strip().split(';')] for row in file.read().split('\n')]
        return M[0][1:], [[cel for cel in row[1:]] for row in M[1:-1]]
    finally:
        file.close()


class _NodesResults():
    def __init__(self, nodes_state:Dict[str, int], specific_nodes:List[str] = None) -> None:
        self._nodes_state_dict = nodes_state
        self._nodes_state      = sorted(nodes_state.items(), key=lambda x: x[1])
        self._specific_nodes   = specific_nodes

    def result(self) -> str:
        pass

class NodesResults(_NodesResults):
    def result(self) -> str:
        return "RESULTS"

class _NodesResultDecorator(_NodesResults):
    def __init__(self, nodes_state: Dict[str, int], nxt_result:_NodesResults) -> None:
        super().__init__(nodes_state)
        self._nxt_result = nxt_result

class MinKnowledgeNode(_NodesResultDecorator):
    def result(self) -> str:
        min_node = self._nodes_state[0]
        txt      = "The less knowledge node is {} with {}".format(min_node[0], min_node[1])
        return txt + '\n' + self._nxt_result.result()

class MaxKnowledgeNode(_NodesResultDecorator):
    def result(self) -> str:
        max_node = self._nodes_state[-1]
        txt      = "The more knowledge node is {} with {}".format(max_node[0], max_node[1])
        return txt + '\n' + self._nxt_result.result()

class PlotNodesHist(_NodesResults):
    def result(self) -> str:
        plt.hist([n[1] for n in self._nodes_state])
        return 'Ploting\n' + self._nxt_result.result()

class SpecificNodesDetail(_NodesResults):
    def result(self) -> str:
        txt = "Specific Nodes Details\n"
        txt += '\n'.join( "{:>5}| {:>10}".format(n[0], n[1]) for n in self._nodes_state)
        return super().result()

if __name__ == "__main__":
    print("MATIRX")
    nodes, adj_matrix = csv_to_matrix('smallworld2.csv')

    graph = Graph(adj_matrix, nodes)
    k, n = graph.propagate(NodesInKnowledgePropagation(nodes))

    print(k, n)