import numpy as np
import pathlib

from typing import Dict, List, Tuple

from .propagation_state import PropagationState

def _csv_to_matrix(name:str) -> Tuple[List[str], List[List[int]]]:
    with open( str(pathlib.Path(__file__).parent.absolute()) + '/../data/input/' + name) as file:
        return [[cel.strip() for cel in row.strip().split(';')] for row in file.read().split('\n')]


class InputGraph():
    def __init__(self, _from:str, name:str) -> None:
        self.name = name

        matrix = _csv_to_matrix(_from)

        self.nodes       = matrix[0][1:]
        self.adjs_matrix = [[int(cel) for cel in row[1:]] for row in matrix[1:-1]]


class Graph():
    def __init__(self, input_graph:InputGraph):
        self._adjs  = input_graph.adjs_matrix
        self._nodes = input_graph.nodes

        N = len(self._nodes)

        self._ones  = np.ones((N, N), dtype=bool)
        self._I     = np.identity(N, dtype=bool)
        
    def propagate(self, cmd:PropagationState, max_steps: int = 1 << 63) -> Tuple[int, Dict[str, int]]:
        cmd.init()

        N = len(self._nodes)
        B = self._I
        M = np.array(self._adjs, dtype = bool) + self._I
        k = 0
        
        nodes_completed = [False] * N
        while not np.array_equal(B, self._ones) and k < max_steps:
            B  = np.matmul(M, B)  # B i+1 = M x B_i 
            k += 1

            for node_i in range(N):
                if not nodes_completed[node_i]:
                    cmd.update(B, node_i)
        
        return k, cmd.result()
