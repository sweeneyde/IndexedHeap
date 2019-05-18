# IndexedHeap
A priority queue implemented as a heap with a supplemental index that allows 
for fast decrease-key operations for Dijkstra's algorithm.

Much of the academic exposition of Dijkstra's Algorithm (such as 
[Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue), or 
[this class page from Darmouth](https://www.cs.dartmouth.edu/~thc/cs10/lectures/0509/0509.html)) 
relies on your priority queue having the ability decrease the key of an entry: 
the priority queue fills up once at the beginning of the algorithm, and then 
exclusively shrinks, with one entry being popped at each loop.

However, the implementation of `PriorityQueue` in the Python's `queue` module has 
no available decrease-key method. Neither does Java's standard library. Probably 
as a result of this, many implementations I see online resort to adding all elements 
immutably to the `priorityQueue` as they're seen, resulting in an unnecessarily large 
heap structure with multiple nodes corresponding to a single vertex. This is asymptotically 
worse: localized decrease-key/siftdown operations with an ever-shrinking heap size should 
be faster than replacing those operations with `heappush`ing and `heappop`ing with a 
potentially much larger heap.

Because I haven't seen many very clear implementations of the `IndexedHeap` structure required 
for a Decrease-Key operation, I wrote one myself, with the goal of being able to write the 
straight-out-of-textbook-pseudocode implementation of Dijkstra's Algorithm that appears in `dijkstra.py`
