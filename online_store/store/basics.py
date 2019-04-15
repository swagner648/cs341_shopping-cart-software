import operator


def unique_set(iterables):
    known_ids = {}
    for it in iterables:
        for element in it:
            if known_ids.get(element.ProductID) is not None:
                known_ids[element.ProductID] += 1
            else:
                known_ids[element.ProductID] = 1
    return [i[0] for i in sorted(known_ids.items(), key=operator.itemgetter(1), reverse=True)]