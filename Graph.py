"""

Graph
- Is a container for Nodes and edges.
- these nodes can be connected, with edges, or can be individual islands( nodes with edges, that are not all connected)

 TODO:
 - setup two graph evaluation types, 1. Directional eg.ICE, 2. All Node Evaluating eg.Dependency Graph
 - a good way of finding islands in the nodes
"""
import Node as mNode


class Graph(object):
    def __init__(self):
        self.nodes = []

    def createNode(self, classType):
        """
        Creates a node of the class type passed in.

        Returns:
            mNode.Node: the newly created node
        """
        node = classType()
        self.nodes.append(node)
        return node

    def getNetworkHeads(self):
        """
        Returns the head nodes of all the networks(islands) in this graph

        Returns:
            []: of nodes
        """
        nodesWithNoConnectedOutput = []

        for node in self.nodes:
            if not node.isConnected():
                nodesWithNoConnectedOutput.append(node)
            else:
                connected = False
                for port in node.portsOut:
                    if port.isConnected():
                        connected = True
                if not connected:
                    nodesWithNoConnectedOutput.append(node)
        return nodesWithNoConnectedOutput

    def getNetworkTails(self):
        """
        Returns the tail nodes of all the networks(islands) in this graph

        Returns:
            []: of nodes
        """
        nodesWithNoConnectedInput = []

        for node in self.nodes:
            if not node.isConnected():
                nodesWithNoConnectedInput.append(node)
            else:
                connected = False
                for port in node.portsIn:
                    if port.isConnected():
                        connected = True
                if not connected:
                    nodesWithNoConnectedInput.append(node)
        return nodesWithNoConnectedInput


