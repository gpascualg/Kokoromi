from __future__ import annotations

from graphviz.dot import graph_head
from .. import stage
from ..pipeline import Pipeline

from diagrams import Cluster, Diagram
from diagrams.aws.network import ELB
from diagrams.programming.flowchart import Action
from diagrams.elastic.agent import Integrations

class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('Visualizer', pipe, config, tuple(), tuple())
        self.all_outputs = []

    def call(self, inputs):
        return {}, True

    @classmethod
    def finish(cls):
        with Diagram("Kokoromi", show=True, direction="TB"):
            with Cluster("Pipeline"):
                pipeline = ELB()

            for test_name, stages in Pipeline.instance().all_pipes:
                with Cluster(test_name):
                    nodes = []
                    for idx, stage in enumerate(stages):
                        with Cluster(f"{stage.name}_{idx}"):
                            nodes.append(Action(
                                width="2", 
                                height="1", 
                                imagescale="false", 
                                fixedsize="true"))

                            [Integrations(
                                plugin.name, 
                                height="0.4", 
                                width="0.4") for plugin in stage.plugins]

                    # Connect one stage to the next
                    for source, dest in zip(nodes, nodes[1:]):
                        source >> dest

                    # Connect pipeline to first stage
                    pipeline >> nodes[0]
