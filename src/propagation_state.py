import numpy as np

from abc    import ABC, abstractmethod
from typing import List

from src.result_processing import Results

class PropagationState(ABC):
    def __init__(self, nodes:List[str]):
        self._nodes       = nodes
        self._nodes_state = []

    @abstractmethod 
    def update(self, graph_state:List[List[int]], index:int):
        pass

    def init(self):
        self._nodes_state = [0] * len(self._nodes)

    def result(self) -> Results:
        result_dict = {self._nodes[i]: self._nodes_state[i] for i in range(len(self._nodes))}
        return Results(result_dict)

class NodesInKnowledgePropagation(PropagationState):
    def update(self, graph_state:List[List[int]], node_i:int):
        self._nodes_state[node_i] = np.sum(graph_state[node_i])
 