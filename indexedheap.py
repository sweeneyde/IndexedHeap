import pyheapq
from collections import defaultdict


class IndexedHeap:
    """A priority queue with the ability to modify existing priority.

    >>> h = IndexedHeap(['1A', '0B', '5C', '2M'])
    >>> h.pop()
    'B'
    >>> h.peek()
    'A'
    >>> h.change_weight('M', '6')
    >>> h.pushpop('W', '7')
    'A'
    >>> h.poppush('R', '8')
    'C'
    >>> [h.pop() for _ in range(len(h))]
    ['M', 'W', 'R']
    """

    def __init__(self, iterable=()):
        self.heap = _IndexedWeightList(map(tuple, iterable))
        pyheapq.heapify(self.heap)

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item):
        return (item in self.heap)

    def push(self, item, weight):
        pyheapq.heappush(self.heap, (weight, item))

    def pop(self):
        weight, item = pyheapq.heappop(self.heap)
        return item

    def peek(self):
        weight, item = self.heap[0]
        return item

    def pushpop(self, item, weight):
        # First push, then pop.
        weight, item2 = pyheapq.heappushpop(self.heap, (weight, item))
        return item2

    def poppush(self, item, weight):
        # First pop, then push.
        weight, item2 = pyheapq.heapreplace(self.heap, (weight, item))
        return item2

    def change_weight(self, item, weight):
        i = self.heap.index(item)
        old_weight, item = self.heap[i]
        self.heap[i] = weight, item
        if weight < old_weight:
            pyheapq.siftdown(self.heap, 0, self.heap.index(item))
        elif weight > old_weight:
            pyheapq.siftup(self.heap, self.heap.index(item))

    def __bool__(self):
        return bool(self.heap)


class _IndexedWeightList(list):
    """A list of (weight, item) pairs, along with the indices of each "item".

    We maintain an auxiliary dict consisting of, for each item, the set of
    indices of that item. Each set will typically have just one index, but
    we do not enforce this because the heapq module updates multiple entries
    at the same time. You could say that this class has all of the
    functionality of priority queue, but without the prioritization.

    >>> arr = _IndexedWeightList(['1A', '0B', '5C', '2M'])
    >>> arr
    _IndexedWeightList(['1A', '0B', '5C', '2M'])
    >>> arr[2]
    '5C'
    >>> arr[0], arr[3] = arr[3], arr[0]
    >>> arr
    _IndexedWeightList(['2M', '0B', '5C', '1A'])
    >>> arr.append('6D')
    >>> arr
    _IndexedWeightList(['2M', '0B', '5C', '1A', '6D'])
    >>> [arr.index(x) for x in 'ABCDM']
    [3, 1, 2, 4, 0]
    >>> arr.remove('B')
    Traceback (most recent call last):
        ...
    TypeError: 'NoneType' object is not callable
    >>> pyheapq.heapify(arr)
    >>> arr.index('B')
    0
    """

    def __init__(self, iterable=()):
        super().__init__(iterable)
        self._index = defaultdict(set)
        for i, (weight, item) in enumerate(super().__iter__()):
            self._index[item].add(i)

    def __setitem__(self, i, pair):
        weight, item = pair
        old_weight, old_item = super().__getitem__(i)
        self._index[old_item].remove(i)
        self._index[item].add(i)
        super().__setitem__(i, pair)

    def index(self, item, start=..., stop=...) -> int:
        only, = self._index[item]
        return only

    def __contains__(self, item):
        return bool(self._index[item])

    def append(self, pair):
        super().append(pair)
        weight, item = pair
        self._index[item].add(len(self) - 1)

    def extend(self, iterable):
        for pair in iterable:
            self.append(pair)

    def pop(self, i=...):
        weight, item = super().pop()
        self._index[item].remove(len(self))
        return weight, item

    def __repr__(self):
        return '{}({})'.format(self.__class__.__qualname__, str(list(self)))

    insert = None
    remove = None
    __delitem__ = None
    sort = None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
