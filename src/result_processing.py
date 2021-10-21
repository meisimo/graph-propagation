from abc        import ABC, abstractmethod
from matplotlib import pyplot as plt
from typing     import Dict, List

class ResultsProcessing(ABC):
    def __init__(self, nodes_state:Dict[str, int], specific_nodes:List[str] = None) -> None:
        self._nodes_state_dict = nodes_state
        self._nodes_state      = sorted(nodes_state.items(), key=lambda x: x[1])
        self._specific_nodes   = specific_nodes

    @abstractmethod
    def output(self) -> str:
        pass

class DummyProcessing(ResultsProcessing):
    def output(self) -> str:
        return "RESULTS"

class _ResultsProcessingDecorator(ResultsProcessing, ABC):
    def __init__(self, nodes_state: Dict[str, int], nxt_result:ResultsProcessing) -> None:
        super().__init__(nodes_state)
        self._nxt_result = nxt_result

class MinKnowledgeNode(_ResultsProcessingDecorator):
    def output(self) -> str:
        min_node = self._nodes_state[0]
        txt      = "The less knowledge node is {} with {}".format(min_node[0], min_node[1])
        return txt + '\n' + self._nxt_result.output()

class MaxKnowledgeNode(_ResultsProcessingDecorator):
    def output(self) -> str:
        max_node = self._nodes_state[-1]
        txt      = "The more knowledge node is {} with {}".format(max_node[0], max_node[1])
        return txt + '\n' + self._nxt_result.output()

class PlotNodesHist(ResultsProcessing):
    def result(self) -> str:
        plt.hist([n[1] for n in self._nodes_state])
        return 'Ploting\n' + self._nxt_result.result()

class SpecificNodesDetail(ResultsProcessing):
    def output(self) -> str:
        txt = "Specific Nodes Details\n"
        txt += '\n'.join( "{:>5}| {:>10}".format(n[0], n[1]) for n in self._nodes_state)
        return super().output()
