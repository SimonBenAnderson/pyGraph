# pyGraph
*Graph based node system, allowing interconnected nodes to
evaluate and perform some computation*

*"Inspired by Maya's Node Graph, Softimages ICE, Houdini"*
***

#### What is pyGraph?
pyGraph is a very vanila implementation of an evaluation node
network. I love node networks, there fun to create in,
and easy to follow what is happening.

***
## TODO
- [x] Create Node
- [x] Create Port
- [x] Create Graph
- [x] Create Test (Test Driven Development)
- [x] Create Edge
- [x] Remove an edge
- [ ] Optimise connected network, to make sure that the node doesn't evaluate if it doesn't have to.
- [ ] Save the network, nodes, ports, edges and values
- [ ] load the network
- [ ] handle islands of nodes( two trees that are not connected ), which island must we evaluate
- [ ] Graph.evaluate -> needs to find the head/heads of each island and perform the evaluate, so that the nodes are all run correctly
- [ ] Create a dirty parameter for ports/nodes, that allows values to record being dirty, and if so only get there upstream evaluated.
- [ ] Parallel/concurrent code, allowing the graph to constantly be evaluating, as you edit nodes. eg evaluation modes-passive-active-at a specific intervals