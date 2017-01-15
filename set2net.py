#!/usr/bin/env python3

# from functools import reduce, partial
# Hacks: I use `sub` to make sets difference
# and `and_` for sets intersection
from operator import sub, and_
from functools import reduce
from copy import deepcopy
from collections import deque
from scipy.special import binom


class Set2NetError(Exception):
    pass


class SetsError(Set2NetError):
    pass


def purge(s, other_sets):
    """
    Substract from the set s the other_sets

    >>> purge({0, 1, 2, 3, 4, 5}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    {5}
    """
    o_s_clone = deque(deepcopy(other_sets))
    o_s_clone.appendleft(s)
    return reduce(sub, o_s_clone)


def intersect_em_all(all_sets):
    """
    Make the intersection of all_sets

    >>> intersect_em_all([{1,2,3,4}, {1,2,3,56,58}, {1,2,56,112}])
    {1, 2}
    """
    return reduce(and_, all_sets)


def intersect_and_purge_by_indx(indexes, all_sets):
    """
    Intersect the sets with index in indexes from all_sets
    and substract the result to the rest of all_sets

    >>> intersect_and_purge_by_indx([1, 2], [{0}, {0,1,2}, {1,2,3}])
    {1, 2}
    """
    to_inte = [all_sets[i] for i in indexes]
    s_i = intersect_em_all(to_inte)
    return purge(s_i, [all_sets[j] for j in range(len(all_sets))
                       if j not in indexes])


def getAccessions(xls_file, sheet_indx=0):
    """
    Returns all Accession Number in an Excel file
    """
    from xlrd import open_workbook
    book = open_workbook(xls_file)
    sheet = book.sheet_by_index(sheet_indx)

    acc_indx = sheet.row_values(0).index('Accession')

    return (acc
            for acc in sheet.col_values(acc_indx, 1))


def polar_dist(n_angles):
    """
    Divide 2*pi in equal angles
    and return the list

    >>> ["%.2f" %(p_c, )  for p_c in polar_dist(4)]
    ['0.00', '1.57', '3.14', '4.71']
    """
    from math import pi
    phi_incr = 2 * pi / n_angles
    return ((i * phi_incr) for i in range(n_angles))


def sum_of_binom(n, k=0):
    """
    To check if the number of intersections is right

    Note: It is possible make an altrenative version
    using math.factorial.
    >>> sum_of_binom(2)
    3
    >>> sum_of_binom(3)
    7
    """
    return sum([int(binom(n, ki)) for ki in range(k, n)])


def transl(val, incr, max_limit, min_limit):
    """
    Cartesian translation from a cartesian system to another,
    that have a maximun limit and a minimun limit.
    Like a coordinate system of a plot.

    >>> transl(0, 10, 15, 8)
    10
    >>> transl(0, 10,  9, 6)
    9
    >>> transl(0,  6, 15, 8)
    8
    """
    val += incr
    if val > max_limit:
        return max_limit
    if val < min_limit:
        return min_limit
    return val


def polar2cart(phi, rho):
    """
    Convert polar coordinates to Cartesian

    >>> from math import pi
    >>> [int(c) for c in polar2cart(0, 1)]
    [1, 0]
    >>> [int(c) for c in polar2cart(0, 2)]
    [2, 0]
    >>> [int(c) for c in polar2cart(3*pi/2, 1)]
    [0, -1]
    """
    from math import cos, sin
    x = rho * cos(phi)
    y = rho * sin(phi)
    return(x, y)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    import os

    from itertools import combinations

    import networkx as nx

    from networkx.readwrite import json_graph
    import json

    from math import sqrt

    # 1. Read excel files

    root = r"../ExampleFile/AnnaMaria_7up"
    _files = [
        "E1004.xls", "E973.xls", "E974.xls",
        "E976.xls", "M917.xls", "M995.xls",
        "WT459.xls"]

    sets = [set(getAccessions(os.path.join(root, f))) for f in _files]

    # 2. Initializing empty graph
    g = nx.Graph()

    # 3. Setting geometric variables

    # rotation, to swich slighty each well
    rot = 0
    # to include also the ray of the circle
    c_ray = 0
    # polar coordinate rho
    rho = 0

    # 4.a Insert nodes inside graph
    # 4.b Positioning them in the space
    # 4.c writing the resulting subsets in a csv file

    # reverse cicle
    for n_sets_to_inters in range(len(sets), 0, -1):
        # obtaining the coordinates of the nodes
        # the heigth of the plot is 500
        # the width is 960
        # for this reason the maximun rho is 250
        n_subsets = int(binom(len(sets), n_sets_to_inters))
        phis = [phi + rot for phi in polar_dist(n_subsets)]

        # `rho` is a fraction of the maximun rho
        # (computed at the end of the cycle)
        # note that the subsets with less intersections
        # are outer
        coords = [polar2cart(phi, rho) for phi in phis]

        # traslate on the screen coordinates,
        # pay attentions to the borders
        coords = list(zip([transl(c[0], 480, 950, 10) for c in coords],
                          [transl(c[1], 250, 490, 10) for c in coords]))

        # I need to know the subsets' `max_size` to
        # adjust the position of the next cycle
        # the update is at the end of the file
        max_size = 0
        for j, c in enumerate(combinations(range(len(sets)),
                                           n_sets_to_inters)):
            # adding a node to the graph
            name = ('_'.join([_files[k][:-4] for k in c]))
            sub_set = intersect_and_purge_by_indx(c, sets)
            size = len(sub_set)
            g.add_node(
                name, size=size,
                group=n_sets_to_inters,
                x=coords[j][0], y=coords[j][1])

            # writing in csv the subset
            with open('../sub_sets/%s.csv' % (name, ), 'wb') as out_file:
                out_file.write(
                    bytes('\n'.join(["%d" % (int(acc),)
                                     for acc in sub_set]), 'UTF-8'))

            # update the max_sixe
            max_size = size if size > max_size else max_size

        # rotate the inner well of an half of the increment of the outer
        # except for the innest one, that has `i` equal to sets.
        if n_sets_to_inters < len(sets):
            rot = phis[1]/2

        # updating `rho`
        c_ray = sqrt(max_size) + 1
        rho += 250/(len(sets)) + c_ray

    def get_group(n):
        return n[1]['group']

    nodes = sorted(g.nodes(data=True), key=get_group)

    # check if the number of nodes generated
    # is as expected
    try:
        assert(len(nodes) == sum_of_binom(len(sets)))
    except AssertError:
        raise SetsError('The number of sets obtained {} is not equal to expected {}'.format(
            len(nodes), sum_of_binom(len(sets))))

    # 5. adding edge to the graph.
    for i, n in enumerate(nodes):
        for m in nodes:
            if (any(part in m[0].split('_') for part in n[0].split('_'))
                    and get_group(n) - get_group(m) == 1):
                g.add_edge(
                    n[0], m[0],
                    value=get_group(m) - get_group(n))

    # 6. write the result in a json
    d = json_graph.node_link_data(g)  # node-link format to serialize
    json.dump(d, open('force/force.json', 'w'), indent=4)
