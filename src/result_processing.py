from abc        import ABC, abstractmethod
from matplotlib import pyplot as plt
from typing     import Dict, List, Tuple


class Results():
    def __init__(
        self,
        nodes_state:Dict[str, int],
    ) -> None:
        self._nodes_state_dict = nodes_state
        self._nodes_state      = sorted(nodes_state.items(), key=lambda x: x[1])
        self._specific_nodes   = None

    @property
    def specific_nodes(self) -> List[str]:
        return self._specific_nodes
    
    @specific_nodes.setter
    def specific_nodes(self, nodes:List[str]):
        self._specific_nodes = nodes

    @property
    def sorted_nodes(self):
        return self._nodes_state
    
    @property
    def nodes(self):
        return self._nodes_state_dict

class ResultsProcessing(ABC):
    def __init__(self, nxt_proc:'ResultsProcessing' = None) -> None:
        self._nxt_proc = nxt_proc

    @abstractmethod
    def _output(self, results:Results) -> str:
        pass

    def output(self, results:Results) -> str:
        if self._nxt_proc:
            return self._nxt_proc._output(results)
        return ""


class _ResultsProcessingDecorator(ResultsProcessing, ABC):
    def __init__(self, nxt_proc:ResultsProcessing = None) -> None:
        super().__init__(nxt_proc)

class MinKnowledgeNode(_ResultsProcessingDecorator):
    def _output(self, results:Results) -> str:
        min_node = results.sorted_nodes[0]
        txt      = "The less knowledge node is {} with {}".format(min_node[0], min_node[1])
        return txt + '\n' + self.output(results)

class MaxKnowledgeNode(_ResultsProcessingDecorator):
    def _output(self, results:Results) -> str:
        max_node = results.sorted_nodes[-1]
        txt      = "The more knowledge node is {} with {}".format(max_node[0], max_node[1])
        return txt + '\n' + self.output(results)

class PlotNodesHist(_ResultsProcessingDecorator):
    def _output(self, results:Results) -> str:
        plt.hist([n[1] for n in results.sorted_nodes])
        return 'Ploting\n' + self.output(results)

class PlotNodesBoxPlot(_ResultsProcessingDecorator):
    def _output(self, results:Results) -> str:
        plt.boxplot([n[1] for n in results.sorted_nodes])
        return 'Ploting\n' + self.output(results)

class SpecificNodesDetail(_ResultsProcessingDecorator):
    def _output(self, results:Results) -> str:
        assert results.specific_nodes, "No specific nodes set"
        txt = "Specific Nodes Details\n"
        txt += '\n'.join( "{:>5}| {:>10}".format(n, results.nodes[n]) for n in results.specific_nodes)
        return txt + '\n' + self.output(results)

class ResultsProcessingFactory():
    MIN_KNOWLEDGE = -1
    MAX_KNOWLEDGE = -2
    HISTOGRAM     = -3
    NODES_DETAILS = -4
    BOXPLOT       = -5

    processes = {
        MIN_KNOWLEDGE: MinKnowledgeNode,
        MAX_KNOWLEDGE: MaxKnowledgeNode,
        HISTOGRAM: PlotNodesHist,
        NODES_DETAILS: SpecificNodesDetail,
        BOXPLOT: PlotNodesBoxPlot,
    }

    @classmethod
    def add_proccessing(cls, *process) -> ResultsProcessing:
        proc = cls.processes[process[0]]()
        for p in process[::-2]:
            proc = cls.processes[p](proc)
        return proc
