# PageRank Estimation

## Projection Description

Within this coursework, I have implemented 2 different methods for estimating pagerank for certain websites

1. Stochastic PageRank - An algorithm that calculates pagerank based on how many visits a page receives during
random walks

2. Distribution-Based PageRank - Uses probability to calculate the probability of being on each page

## Features

Implements two PageRank estimation algorithms:
Stochastic PageRank using random walkers. 
Distribution-Based PageRank using probability updates. 
Command-line interface to select the method and control parameters.
Displays top-ranked pages and their PageRank values.
Prints number of nodes and edges about the graph 

## Commands

python page_rank.py school_web2024-1.txt -m stochastic -r 1000000 -n 10
 