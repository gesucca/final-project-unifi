import glob
import os

from collections import deque


def unusual_pattern(filename):

    with open('unusual_pattern.res', 'a') as the_file:
        the_file.write('file: ' + filename + '\n')

    with open(filename) as fileobj:
        for line in fileobj:
            if '{' in line:
                seq = line.split('{')
                seq = deque(seq)
                seq.popleft()
                seq.pop()

                clean_seq = []
                for token in seq:
                    index = token.rfind('_')
                    clean_seq.append(token[:index])

                sortedSeq = sorted(clean_seq)

                if sortedSeq != clean_seq:
                    with open('unusual_pattern.res', 'a') as the_file:
                        the_file.write(line + '\n')

        with open('unusual_pattern.res', 'a') as the_file:
            the_file.write('### end\n\n')


with open('unusual_pattern.res', 'w') as the_file:
    the_file.write('UNUSUAL PATTERN ANALYSIS\n')
    the_file.write('Non sorted frequent sequences will be printed here.\n')
    the_file.write('\n')


for file in glob.glob("*.txt"):
    unusual_pattern(file)
