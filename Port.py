class Port(object):
    def __init__(self, name="port", node=None, defaultValue=None):
        """
        :param name:
        :param node:
        :param defaultValue:

        Args:
            edges ([]): is a list of ports that this port is connected to
        """
        self.name = name
        self.node = node
        self.value = defaultValue # maybe have this as a property, that if isConnected then is queries the connected port
        self.edges = []

    def isConnected(self):
        if len(self.edges):
            return True
        return False

    def isSource(self):
        pass

    def isDestination(self):
        pass

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

        self.edges.append(destPort)
        destPort.edges.append(self)
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
            self.edges = []
        else:
            for port in self.edges:
                if port == discPort:
                    self.edges.remove(port)
                    port.disconnect(self)
