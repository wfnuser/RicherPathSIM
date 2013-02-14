import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.BareBonesHelper import  getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore

__author__ = 'jontedesco'

class NeighborSimAPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, paper, adjMatrix, extraData):

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, paper, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % paper)
        mostSimilarTable = texttable.Texttable()
        rows = [['Paper', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


if __name__ == '__main__':
    experiment = NeighborSimAPPAExperiment(
        None, 'Most Similar APPA NeighborSim Authors', outputFilePath='results/appaNeighborSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithHalfCitations')))
    appaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper'])

    # Run for all authors
    experiment.runFor('Christos Faloutsos', appaAdjMatrix, extraData)
    experiment.runFor('Jiawei Han', appaAdjMatrix, extraData)
    experiment.runFor('Sergey Brin', appaAdjMatrix, extraData)
    experiment.runFor('Sanjay Ghemawat', appaAdjMatrix, extraData)