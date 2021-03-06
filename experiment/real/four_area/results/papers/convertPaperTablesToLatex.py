from collections import defaultdict
import os

__author__ = 'jontedesco'

allowSplitTitles = False

# Construct the dictionary of number of citations for each paper
paperCitationFile = open('../../../data/paperCitationCounts')
citationCounts = defaultdict(int)
for line in paperCitationFile:
    index = line.find(': ')
    count, title = line[:index], line[index+2:]
    title = title.strip().replace(' ', '')
    citationCounts[title] = int(count)

for filename in os.listdir('.'):
    if 'PathSim' not in filename and 'NeighborSim' not in filename: continue
    measure = 'PathSim' if 'PathSim' in filename else 'NeighborSim'
    content = open(filename).read()
    latexContent = ""

    titleBuffer = ""
    score = 0
    rank = 0

    for line in content.split('\n'):
        if line.startswith('Most Similar'):
            rank = 0
            latexContent += '\hline\n\end{tabular}\n\n'
            latexContent += '\\begin{tabular}{|c|c|c|c|}\n\hline\nRank & Paper & Citations \\footnotemark[1] ' + \
                            '& %s Score\\\\\n\hline\n' % measure
        elif 'Paper' in line:
            continue
        elif line.startswith('| '):
            tokens = line[1:].split('|')
            titleBuffer += ' ' + tokens[0].strip()
            if len(tokens[1].strip()) > 0: score = float(tokens[1].strip())
        elif line.startswith('+-') and len(titleBuffer) > 0:
            rank += 1
            strippedTitle = titleBuffer.strip().replace(' ','')
            title = titleBuffer.strip().rstrip('.')

            firstHalf = title
            splitTitle = (len(title) > 40) and allowSplitTitles
            if splitTitle:
                titleParts = title.split()
                firstHalf = ' '.join(titleParts[:len(titleParts) / 2])
                secondHalf = ' '.join(titleParts[len(titleParts) / 2:])

            if rank == 1:
                latexContent += '\\textbf{%d} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} \\\\\n' % (
                    rank, firstHalf, citationCounts[strippedTitle], score
                )
            else:
                latexContent += '%d & %s & %s & %s \\\\\n' % (rank, firstHalf, citationCounts[strippedTitle], score)

            # Handle the second half of the title, if it was split
            if splitTitle:
                if rank == 1:
                    latexContent += ' & \\textbf{%s} &  &  \\\\\n' % secondHalf
                else:
                    latexContent += ' & %s &  &  \\\\\n' % secondHalf

            titleBuffer = ""
            score = 0
    with open(os.path.join('latex', filename), 'w') as outputFile:
        outputFile.write(latexContent)
