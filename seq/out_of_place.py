from collections import deque
import re

out_of_place = {}
debug = False


def get_order(list, index):
    sliced = list[index]
    sliced = sliced[:4]
    return re.sub("[^0-9]", "", sliced)


def prepare_list(line):
    line = line.split('{')
    line = deque(line)
    line.popleft()
    line.pop()
    return list(line)


def proportion():
    tot = 0

    for k in out_of_place:
        tot = tot + out_of_place[k]

    for k in out_of_place:
        out_of_place[k] = round(out_of_place[k] * 100 / tot, 2)


with open("seq/unusual_pattern.res") as fileobj:
    for line in fileobj:

        if debug:
            print('---------------------------------')
            print('line:')
            print(line)

        if '{' in line:
            seq = prepare_list(line)

            if debug:
                print('seq:')
                print(seq)

            first = get_order(seq, 0)

            for i in range(1, len(seq)):
                if debug:
                    print('first:')
                    print(first)
                    print('current:')
                    print(get_order(seq, i))
                    print('current<first:')
                    print(get_order(seq, i) < first)
                    print('key:')
                    print(seq[i])

                if get_order(seq, i) < first:
                    key = re.sub("}", "", seq[i])
                    out_of_place[key] = out_of_place.get(key, 0) + 1
                else:
                    first = get_order(seq, i)

proportion()
print(out_of_place)
