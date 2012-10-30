import cProfile
import os
from time import time
from experiment.Experiment import Experiment
from experiment.helper.ExperimentHelper import ExperimentHelper
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy

__author__ = 'jontedesco'

class AuthorPathSimFourAreaProfiler(Experiment):
    def run(self):
        strategy = PathSimStrategy(self.graph, [Author, Paper, Author], True)
        experimentHelper = ExperimentHelper()

        # Get the author node for 'Christos Faloutsos)
        authors = experimentHelper.getNodesByAttribute(self.graph, 'name', 'Christos Faloutsos')
        assert(len(authors) == 1)
        christos = list(authors)[0]
        number = 10

        # Output the top ten most similar authors on the APA meta path
        before = time()
        strategy.findMostSimilarNodes(christos, number)
        after = time()
        runningTime = after - before
        self.output("Total time (seconds): %4.4f" % runningTime)


if __name__ == '__main__':
    experiment = AuthorPathSimFourAreaProfiler(
        os.path.join('graphs', 'fourArea'),
        'Author PathSim Similarity on Four Area dataset'
    )
    cProfile.run('experiment.run()')
