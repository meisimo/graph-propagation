from src.graph import InputGraph, Graph
from src.propagation_state import NodesInKnowledgePropagation
from src.result_processing import MinKnowledgeNode, ResultsProcessingFactory

input_graph    = InputGraph(_from="smallworld2.csv", name="Small world")
graph          = Graph(input_graph)
steps, results = graph.propagate(NodesInKnowledgePropagation(input_graph.nodes), 4)

proc = ResultsProcessingFactory.add_proccessing(
    results,
    ResultsProcessingFactory.MIN_KNOWLEDGE,
    ResultsProcessingFactory.MAX_KNOWLEDGE,
)

print(steps)
print(proc.output())

