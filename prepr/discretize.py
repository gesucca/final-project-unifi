"""Discretization of countinous attributes in datasets."""

ONE_TO_TEN_DISCR = {'0-4': [0, 4], '4-6': [4, 6], '6-8': [6, 8], '8-10': [8, 10], 'MAX': 10}
# choose right ranges!

# this sucks, find a clever way
def discretize(source, dest):
    for doc in source.find():
        if doc['Media'] == 'n.c.':
            doc['Media'] = 'NOT_AVAILABLE'
            dest.insert_one(doc)
            return
        if doc['Media'] <= ONE_TO_TEN_DISCR['MAX']:
            if doc['Media'] > ONE_TO_TEN_DISCR['0-4'][0] and doc['Media'] <= ONE_TO_TEN_DISCR['0-4'][1] or doc['Media'] == 'n.c.':
                doc['Media'] = '0-4'
            if doc['Media'] > ONE_TO_TEN_DISCR['8-10'][0] and doc['Media'] <= ONE_TO_TEN_DISCR['8-10'][1]:
                doc['Media'] = '8-10'
        dest.insert_one(doc)
