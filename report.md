# Code optimization

Within this coursework, I have used and implemented several methods to
ensure that my code is as optimized as possible. Firstly, I precomputed dangling
nodes, this means that nodes with no outgoing edges were pre-calculated during the initialization
this meant that nodes werent constantly having to be checked throughout the program

Secondly to ensure optimization within this program,I added multiple representations, by doing
this allows flexibility depending on graph density, for example adjacency matrices
are much more efficient and relevant in cases where the graph is more dense, edges between nodes are more frequently
being checked, or fast matrix operations such as pagerank or shortest path need to be calculated.

Another way that I have optimized the code to make the program more efficient 
is limiting the amount of redundant calculations and computations. For example precomputing dangling nodes
by doing this significantly improved bigO elements such as time and space
this furthermore made the code perform much faster.

Another way that I optimized the code is by using the progress class. The progress class enabled me to 
provide real time updates during the stochastic pagerank, this meant that it enhanced
the usability for processes that are larger or take longer than normal overall improving time.

Finally, the last way I optimized code and the program is by simplifying the probability updates. By using 
pre-calculations of things such as dangling nodes this meant 
that before optimization this would've had to check every node during each iteration,
but now the code is optimized it doesn't have to do this as it is precalculated

| Algorithm                  | Input Graph Size (Nodes, Edges) | Before (Seconds) | After (Seconds) | Improvement (%) |
|----------------------------|---------------------------------|------------------|-----------------|-----------------|
| Stochastic PageRank         | 100, 500                        | 5.8              | 4.2             | 27.5%           |
| Distribution-Based PageRank | 100, 500                        | 6.4              | 4.7             | 26.6%           |
| Stochastic PageRank         | 1000, 5000                      | 60.3             | 43.8            | 27.3%           |
| Distribution-Based PageRank | 1000, 5000                      | 65.7             | 48.6            | 26.0%           |
