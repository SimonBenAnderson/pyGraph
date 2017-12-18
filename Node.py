import Port as port
class Node(object):
    def __init__(self):
        """
        type: The type of node that this node is.
         id: is the nodes instance id, this should be unique for each node in the graph, and is not serialized.
        name: The name of this node, allowing users to rename there node
        portsIn: List of input ports
        portsOut: List of output ports
        dirty: if the node has had some values updated on it, then it gets flagged as dirty
        """
        self.type = ""
        self.id = -1
        self.name = ""
        self.portsIn = []
        self.portsOut = []
        self._dirty = True

        self.initInputPorts()
        self.initOutputPorts()


    """
    dirty property
    This property is used to check if the node contains any ports 
    that are dirty, or connection to nodes that are dirty.
    
    How to clean the node:
    When a node is evaluated, all input ports should be checked to 
    see if they are clean, if they are all clean then set the node 
    to be clean by setting the self._dirty = true
    """
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, val):
        # if setting the node to be dirty, all conncted nodes up stream must be have there
        # connected inputs set to dirty as well.
        if self._dirty == False and val:
            for port in self.portsOut:
                for edgePort in port.edges:
                    edgePort.setDirty()
        self._dirty = val

    def initInputPorts(self):
        """
        MUST OVERRIDE

        This method is used to place all input port initialisation for your node
        """
        pass

    def initOutputPorts(self):
        """
        MUST OVERRIDE

        This method is used to place all output port initialisation for your node
        """
        pass

    def evaluate(self):
        """
        MUST BE OVERLOADED

        This method executes the node, reading the inputs and performing what ever computations on the inputs,
        then sends it to the output ports
        """
        pass

    def getInputPort(self, name):
        """
        Finds the port from the port list that has this name, else returns None

        Args:
            name (str): Name of the port you are wanting to return

        Returns:
             Port: The port with the matching name
        """
        for port in self.portsIn:
            if port.name == name:
                return port
        return None

    def getOutputPort(self, name):
        for port in self.portsOut:
            if port.name == name:
                return port
        return None

    def addInputPort(self, name, value=0.0):
        """
        Creates a new input port on the node

        Args:
            name(str): The name of the port
            value(float): The value of the port
        Returns:
            Port: The newly created port
        """
        newPort = port.Port(name, self, value)
        self.portsIn.append(newPort)
        return newPort

    def addOutputPort(self, name):
        newPort = port.Port(name, self)
        self.portsOut.append(newPort)
        return newPort

    def isConnected(self):
        """
        Checks all ports to see if any are connected, if a connection is found, then returns true
        """
        for port in self.portsIn + self.portsOut:
            if port.isConnected():
                return True
        return False

    def evaluateConnection(self):
        for port in self.portsIn:
            if port.dirty:
                if port.isConnected():
                    port.edges[0].node.evaluate()
                    port.value = port.edges[0].value
                port.dirty = False

    def __repr__(self):
        return "{} > Input Ports: {}  OutputPorts:{}".format(self.type, len(self.portsIn), len(self.portsOut))

# CONSTANT NODES

class SumNode(Node):
    def __init__(self):
        super(SumNode,self).__init__()
        self.type = self.__class__.__name__

    def initInputPorts(self):
        # initialise Input Ports
        self.addInputPort(name="value1")
        self.addInputPort(name="value2")

    def initOutputPorts(self):
        # initialise Output Ports
        self.addOutputPort(name="result")

    def evaluate(self):
        """
        Performs the computation of the node and updates the output ports
        """
        if self.dirty:
            self.evaluateConnection()

            sum = 0
            for port in self.portsIn:
                sum += port.value
            self.portsOut[0].value = sum
            self.dirty=False

class NegateNode(Node):
    def __init__(self):
        super(NegateNode, self).__init__()
        self.type = self.__class__.__name__

    def initInputPorts(self):
        self.addInputPort("value")

    def initOutputPorts(self):
        self.addOutputPort("result")

    def evaluate(self):
        # only evaluates the node if it is dirty
        if self.dirty:
            self.evaluateConnection()
            self.portsOut[0].value = -self.portsIn[0].value
            self.dirty=False

class SubtractNode(Node):
    def __init__(self):
        super(SubtractNode, self).__init__()
        self.type = self.__class__.__name__

    def initInputPorts(self):
        # initialise Input Ports
        self.addInputPort(name="value1")
        self.addInputPort(name="value2")

    def initOutputPorts(self):
        # initialise Output Ports
        self.addOutputPort(name="result")

    def evaluate(self):
        # only evaluates the node if it is dirty
        if self.dirty:
            self.evaluateConnection()

            # TODO: move just the evaluation code into a function and have
            # all the dirty and updating of the ports to outside of this function
            value = self.portsIn[0].value
            for port in self.portsIn[1:]:
                value -= port.value

            self.portsOut[0].value = value
            self.dirty = False

class MultiplyNode(Node):
    def __init__(self):
        super(MultiplyNode, self).__init__()
        self.type = self.__class__.__name__

    def initInputPorts(self):
        # initialise Input Ports
        self.addInputPort(name="value1")
        self.addInputPort(name="value2")

    def initOutputPorts(self):
        # initialise Output Ports
        self.addOutputPort(name="result")

    def evaluate(self):
        # only evaluates the node if it is dirty
        if self.dirty:
            self.evaluateConnection()
            val = self.portsIn[0].value
            for port in self.portsIn[1:]:
                val *= port.value

            self.portsOut[0].value = val
            self.dirty = False

"""
Container Node:
This node, is used to create a node which is actually multiple 
interconnected nodes, performing a specific task. Instead of coding 
a node, you can create a node from interconnected Nodes.

Users create there own input and output ports.

Port Structure:
Internal input and output Ports, that the contained nodes will connect to,
to access data from outside the container, and send data outside of the container
When a port is added to this node, an opposite port with the same name will be added 
to the internal ports.
"""
#TODO: Add some checks to make sure when you remove a node, it is no longer connected to any node inside of the container
#TODO: need to alter the ports for a container else, you end up with and output port, connected to an output port, and then an infinit dirty update loop occurs
class ContainerNode(Node):
    internalNodes = []

    def __init__(self):
        super(ContainerNode, self).__init__()
        self.type = self.__class__.__name__

    def evaluate(self):
        if self.dirty:
            self.evaluateConnection()

            # evaluate internal connections
            for port in self.portsIn:
                for edge in port.internalEdges:
                    edge.value = port.value
                    edge.dirty = False
                    port.dirty = False

            for port in self.portsOut:
                port.internalEdges[0].node.evaluate()
                port.value = port.internalEdges[0].value
                port.dirty = False

            self.dirty = False

    def addNode(self, node):
        self.internalNodes.append(node)

    def createNode(self, nodeType):
        newNode = nodeType()
        self.internalNodes.append(newNode)
        return newNode

    def removeNode(self, node):
        self.internalNodes.remove(node)

    def addInputPort(self, name, value=0.0):
        newPort = port.ContainerPort(name, self, value)
        self.portsIn.append(newPort)
        return newPort

    def addOutputPort(self, name):
        newPort = port.ContainerPort(name, self)
        self.portsOut.append(newPort)
        return newPort