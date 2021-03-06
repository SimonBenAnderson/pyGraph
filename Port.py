class Port(object):
    def __init__(self, name="port", node=None, defaultValue=None):
        """
        :param name:
        :param node:
        :param defaultValue:

        Args:
            edges ([]): is a list of ports that this port is connected to
            dirty (bool): if the value of this Port has been updated then the node is set to dirty
        """
        self.name = name
        self.node = node
        self._value = defaultValue # maybe have this as a property, that if isConnected then is queries the connected port
        self.defaultValue = defaultValue
        self.edges = []
        self.dirty = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.setDirty()

    def isConnected(self):
        if len(self.edges):
            return True
        return False

    def isSource(self):
        pass

    def isDestination(self):
        pass

    def addEdge(self, port):
        self.edges.append(port)

    def setDirty(self):
        """
        Sets the port and the ports node to be dirty
        """
        self.dirty = True
        self.node.dirty = True

    def connect(self, destPort):
        """
        Create a connection between the current port and a destination port

        Args:
            destPort(Port): The port that this port will be connecting to.

        Returns:
            bool: False if the connection failed, true if the connection was made successfully
        """
        if destPort.isConnected():
            return False

        self.addEdge(destPort)
        destPort.addEdge(self)
        # as the port has been connected, the connected node has to be updated
        destPort.setDirty()
        self.setDirty()
        return True

    def disconnect(self, discPort=None):
        """
        Disconnect this port from another port. If no port is given, then disconnects all connection to this port
        As each edge(connection) has two ports and each port stores the port it is connected to, we have to remove the each port
        from storing one another

        Args:
            discPort (Port): The port we will be disconnecting from
        """

        if discPort is None:
            for port in self.edges:
                port.disconnect(self)
                port.setDirty()
            self.edges = []
        else:
            for port in self.edges:
                if port == discPort:
                    self.edges.remove(port)
                    port.disconnect(self)
                    port.setDirty()

class ContainerPort(Port):
    def __init__(self, name="port", node=None, defaultValue=None):
        super(ContainerPort, self).__init__(name, node, defaultValue)
        self.internalEdges = []

    def addEdge(self, port):
        if port.node in self.node.internalNodes:
            self.internalEdges.append(port)
            #self.value = port.value
        else:
            self.edges.append(port)

    def isConnected(self):
        if len(self.edges):
            return True
        return False

    def connect(self, destPort):
        """
        Create a connection between the current port and a destination port

        Args:
            destPort(Port): The port that this port will be connecting to.

        Returns:
            bool: False if the connection failed, true if the connection was made successfully
        """
        if destPort.isConnected():
            return False

        self.addEdge(destPort)
        destPort.addEdge(self)
        # as the port has been connected, the connected node has to be updated
        destPort.setDirty()

        return True

    def disconnect(self, discPort=None):
        """
        Disconnect this port from another port. If no port is given, then disconnects all connection to this port
        As each edge(connection) has two ports and each port stores the port it is connected to, we have to remove the each port
        from storing one another

        Args:
            discPort (Port): The port we will be disconnecting from
        """

        if discPort is None:
            for port in self.edges:
                port.disconnect(self)
                port.setDirty()
            self.edges = []
        else:
            for port in self.edges:
                if port == discPort:
                    self.edges.remove(port)
                    port.disconnect(self)
                    port.setDirty()
