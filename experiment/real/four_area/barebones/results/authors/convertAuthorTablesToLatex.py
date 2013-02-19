import os

__author__ = 'jontedesco'

for filename in os.listdir('.'):
    if 'PathSim' not in filename and 'NeighborSim' not in filename: continue
    measure = 'PathSim' if 'PathSim' in filename else 'NeighborSim'
    content = open(filename).read()
    latexContent = ""
    for line in content.split('\n'):
        if line.startswith('Most Similar'):
            rank = 0
            latexContent += '\hline\n\end{tabular}\n\n'
            latexContent += '\\begin{tabular}{|c|c|c|c|}\n\hline\nRank & Author & Citations & %s Score\\\\\n\hline\n' % measure
        elif line.startswith('+='):
            continue
        elif 'Author' in line:
            continue
        elif line.startswith('| '):
            rank += 1
            tokens = line[1:].split('|')
            author = tokens[0].strip()
            score = tokens[1].strip()
            citations = tokens[2].strip()
            latexContent += '%d & %s & %s & %s \\\\\n' % (rank, author, citations, score)
    with open(os.path.join('latex', filename), 'w') as outputFile:
        outputFile.write(latexContent)
