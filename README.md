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
- [x] Create a dirty parameter for ports/nodes, that allows values to record being dirty, and if so only get there upstream evaluated.
- [ ] Parallel/concurrent code, allowing the graph to constantly be evaluating, as you edit nodes. eg evaluation modes-passive-active-at a specific intervals

## DIRTY IMPLEMENTATION
*The current design for how ports and nodes become dirty and how that data is used throughout the network*

- When a value in a port gets updated manually (ie setting the value), then the port and the node on which the port exists gets set to dirty.
- Currently my thought are that when a port/node gets set to dirty, the connected node upstream(connected to output port) 
get set to dirty, and this travels up all the way to the head. The reason for this is we can just check all the head nodes,
 and if any are set to dirty we can trace that down through the dirty nodes in the graph. **Other Option:** would be to traverse the entire tree 
 and see if any ports are dirty, and then if any dirty nodes are found, then traverse the nodes from the dirty node to the head.
 
- **Alternate Implementaion:** Store all dirty nodes in a reference list. Then traverse the nodes 
until you find a shared node ( two dirty node networks connect to the same node), 
and compute only up to that node, then once both ports are updated continue with 
the evaluation till you reach the end.

- **TEST IMPLEMENTED:** I created another branch that did not have the dirty flags implemented, and ran over a node network 100 times, evaluating the
head nodes. The graph with the dirty parameters took 0.49ms while the graph with no dirty parameters took 1.766ms to complete the same 100 evaluations.