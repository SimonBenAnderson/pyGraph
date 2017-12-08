"""

Graph
- Is a container for Nodes and edges.
- these nodes can be connected, with edges, or can be individual islands( nodes with edges, that are not all connected)

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

class Edge(object):
    def __init__(self):
        self.sourcePort
        self.destinationPort

    @classmethod
    def connect(cls, srcPort, dstPort, force=False):
        """
        Connect two ports together, One can only c
        Args:
            srcPort (Port): port you will be connecting from.
            dstPort (Port): port you will be connecting too.
            force (bool): If you want to force the connection, disconnecting a connection that did exist

        Returns:
            bool: The return value. True is successful, False if connection failed
        """
        pass