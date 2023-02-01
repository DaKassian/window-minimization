# window-minimization
Python code for window and edge length minimization algorithms of my bachelor thesis

Abstract:

Visualization of bipartite graphs in easy-to-read drawings is a challenging task.
Consider a network graph of international companies and all the countries they operate in.
A large number of nodes affects legibility, so a good-looking drawing is required.
We consider drawings in which the nodes of the two partitions are drawn on two separate curves; either two horizontal lines or two concentric circles.
There are several factors that affect readability. 
One such factor is the length of the edges in the drawing.

Another factor is the window size, where the window of a node is the smallest interval, either x-interval or angular interval, whose image on the two curves contains both the position of the node and the position of its neighbors.

In this thesis, we use two techniques to improve these factors:
First, from a given drawing of a bipartite graph, we either move the nodes of one partition to the positions where the window size or edge length is minimal while keeping the other partition fixed or move the nodes in both partitions.
The former technique is, with restrictions, feasible, while the latter is \np-complete.

After that, we introduce an unconventional way of visualizing bipartite graphs by placing the partitions on the boundaries of an annulus.
We present an algorithm that computes the best inner-to-outer-radius ratio to draw straight edges without intersecting the inner circle.
