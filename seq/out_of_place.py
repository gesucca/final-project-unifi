from collections import deque
import re

out_of_place = {}


def get_order(list, index):
    return re.sub("[^0-9]", "", list[index])


def prepare_list(line):
    line = line.split('{')
    line = deque(line)
    line.popleft()
    line.pop()
    return list(line)


with open("seq/unusual_pattern.res") as fileobj:
    for line in fileobj:
        if '{' in line:
            seq = prepare_list(line)

            first = get_order(seq, 0)
            for i in range(1, len(seq)):
                if get_order(seq, i) < first:
                    key = re.sub("}", "", seq[i])
                    out_of_place[key] = out_of_place.get(key, 0) + 1
                else:
                    first = get_order(seq, i)

print(out_of_place)
