from collections import defaultdict
from math import inf
from indexedheap import IndexedHeap


class Graph:
    """ A nonnegatively weighted, directed multigraph.

    Stored as a list of outgoing edges for each vertex.

    >>> g = Graph()
    >>> for source, dest, weight in [ \
            ('a', 'b', 7), ('a', 'b', 8), ('a', 'c', 9), ('a', 'f', 14), \
            ('b', 'c', 10), ('b', 'd', 15), ('c', 'd', 11), ('c', 'f', 2), \
            ('d', 'e', 6), ('e', 'f', 9), ('f', 'g', 100), ('g', 'b', 100), \
            ('a', 'a', 100) \
        ]: \
            g.add_edge(source, dest, weight)
    >>> g.distance_and_shortest_path('a', 'f')
    (11, ['a', 'c', 'f'])
    >>> g.distance_and_shortest_path('b', 'e')
    (21, ['b', 'd', 'e'])
    >>> g.distance_and_shortest_path('a', 'a')
    (0, ['a'])
    >>> g.distance_and_shortest_path('f', 'a')
    (inf, None)
    >>> g.distance_and_shortest_path('garbage', 'junk')
    (inf, None)
    """

    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(list)

    def add_edge(self, source, destination, weight):
        """ Add a weighted edge from source to destination.
        """
        if weight < 0:
            raise ValueError("Edge weights cannot be negative.")
        self.vertices |= {destination, source}
        self.edges[source].append((destination, weight))

    def distance_and_shortest_path(self, source, destination):
        """Find the lightest-weighted path from source to destination.

        We use Dijkstra's algorithm with an indexed heap.

        :return: A 2-tuple (d, [v0, v1, ..., vn]),
            where v0==source and vn==destination.
        """
        if not {source, destination} <= self.vertices:
            return inf, None

        # For each vertex v, store the weight of the shortest path to found
        # so far to v, along with v's predecessor in that path.
        distance = {v: inf for v in self.vertices}
        distance[source] = 0
        predecessor = {}

        # A priority queue of exactly the unexplored vertices,
        h = IndexedHeap((distance[v], v) for v in self.vertices)

        # Explore until all vertices closer to source have been exhausted,
        # at which point we will have already found the shortest path (if any) to destination.
        while h.peek() != destination:
            v = h.pop()
            v_dist = distance[v]
            for neighbor, edge_weight in self.edges[v]:
                # We've found a new path to neighbor. If the distance along
                # this new path (through v) is better than previously found,
                # then "relax" the stored distance to that along the new path.
                alt_dist = v_dist + edge_weight
                if alt_dist < distance[neighbor]:
                    distance[neighbor] = alt_dist
                    predecessor[neighbor] = v
                    h.change_weight(neighbor, alt_dist)

        if distance[destination] == inf:
            # No path was found.
            return inf, None

        # Trace back the predecessors to get the path.
        path = [destination]
        while path[-1] != source:
            path.append(predecessor[path[-1]])
        path.reverse()
        return distance[destination], path


if __name__ == "__main__":
    import doctest

    doctest.testmod()
