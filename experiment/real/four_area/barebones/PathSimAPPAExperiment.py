import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.BareBonesHelper import  getMetaPathAdjacencyData, findMostSimilarNodes

__author__ = 'jontedesco'

class PathSimAPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData):

        # Find the top 10 most similar nodes to some given node
        mostSimilar = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


if __name__ == '__main__':
    experiment = PathSimAPPAExperiment(
        None, 'Most Similar APPA PathSim Authors', outputFilePath='results/appaPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithHalfCitations')))
    appaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'author'])

    # Run for all authors
    experiment.runFor('Christos Faloutsos', appaAdjMatrix, extraData)
    experiment.runFor('Jiawei Han', appaAdjMatrix, extraData)
    experiment.runFor('Sergey Brin', appaAdjMatrix, extraData)
    experiment.runFor('Sanjay Ghemawat', appaAdjMatrix, extraData)