import unittest
import Node as mNode
import Graph as mGraph

# TODO: Add dirty command to the node, allowing a check to bypass all the computations

"""
Test Node, is for testing all node types, making sure that the node itself is working correctly
    - Sum Node
    - Negate Node
"""
class TestNode(unittest.TestCase):

    # These are overridden methods, for "test fixtures". Allowing one to setup specific data/remove specific data
    #  - At the moment we have no use for these.
    def setUp(self):
        pass
    def tearDown(self):
        pass

    # tests the sumNode executes correctly
    def test_SumNode(self):
        sumNode = mNode.SumNode()
        sumNode.portsIn[0].value = 5.5
        sumNode.portsIn[1].value = 10.0
        # adds a new port
        newPort = sumNode.addInputPort("value3")
        newPort.value = 0.5
        # evaluates port
        sumNode.evaluate()
        self.assertEqual(sumNode.portsOut[0].value, 16.0)

    def test_NegateNode(self):
        negNode = mNode.NegateNode()
        negNode.portsIn[0].value = 20
        negNode.evaluate()
        self.assertEqual(negNode.portsOut[0].value, -20)

"""
Test pyGraph
- Checks a node gets created correctly
- Checks a simple 2 node connection works, daiseyChain (2 nodes)
- Checks a simple 3 node connection works, 2 nodes connected to one (3 nodes)
- Check 1 node connected to 2 nodes, evaluation and checking data flow works
"""
class TestPyGraph(unittest.TestCase):
    def test_GraphNodeCreation(self):
        # create a graph instance
        graph = mGraph.Graph()
        node = graph.createNode(mNode.SumNode)
        # checks the amount of nodes in the graph is one
        self.assertEqual(len(graph.nodes), 1)

    def test_Simple2NodeEdgeConnection(self):
        """
        2 Nodes are connected by one edge (port to port)
        """
        graph = mGraph.Graph()
        sumNode_1 = graph.createNode(mNode.SumNode)
        sumNode_2 = graph.createNode(mNode.SumNode)

        edgeCreated = sumNode_1.getOutputPort("result").connect(sumNode_2.getInputPort("value1"))
        self.assertTrue(edgeCreated)

        sumNode_1.portsIn[0].value = 2.0
        sumNode_1.portsIn[1].value = 1.5
        sumNode_2.portsIn[0].value = 3.0
        sumNode_2.portsIn[1].value = 5.25

        sumNode_1.evaluate()
        sumNode_1.portsIn[0].value = 12.0
        sumNode_2.evaluate()

        self.assertEqual(sumNode_1.portsOut[0].value, 13.5, "Output of SumNode1 is incorrect")
        self.assertEqual(sumNode_2.portsOut[0].value, 18.75, "Output of SumNode2 is incorrect")

    def test_Simple3NodeDaiseyChain(self):
        """
        3 Nodes are connected in a daisey chain structure, one after another
        """
        graph = mGraph.Graph()
        sumNode_1 = graph.createNode(mNode.SumNode)
        sumNode_2 = graph.createNode(mNode.SumNode)
        sumNode_3 = graph.createNode(mNode.SumNode)

        edgeCreated = sumNode_1.getOutputPort("result").connect(sumNode_2.getInputPort("value1"))
        self.assertTrue(edgeCreated)
        edgeCreated = sumNode_2.getOutputPort("result").connect(sumNode_3.getInputPort("value1"))
        self.assertTrue(edgeCreated)

        sumNode_1.portsIn[0].value = 1.0
        sumNode_1.portsIn[1].value = 1.5
        sumNode_2.portsIn[0].value = 2.0
        sumNode_2.portsIn[1].value = 2.25
        sumNode_3.portsIn[0].value = 3.0
        sumNode_3.portsIn[1].value = 3.25

        sumNode_3.evaluate()

        self.assertEqual(sumNode_3.portsOut[0].value, 8.0, "Output from Node 3 incorrect")

    def test_3NodeFork(self):
        """
        3 Nodes are connected in a daisey chain structure, one after another

        |node_1|--
                   \
                     --> |sumNode_3| --> |negateNode|
                   /
        |node_2|--

        """
        graph = mGraph.Graph()
        sumNode_1 = graph.createNode(mNode.SumNode)
        sumNode_2 = graph.createNode(mNode.SumNode)
        sumNode_3 = graph.createNode(mNode.SumNode)

        edgeCreated = sumNode_1.getOutputPort("result").connect(sumNode_3.getInputPort("value1"))
        self.assertTrue(edgeCreated)
        edgeCreated = sumNode_2.getOutputPort("result").connect(sumNode_3.getInputPort("value2"))
        self.assertTrue(edgeCreated)

        sumNode_1.portsIn[0].value = 1.0
        sumNode_1.portsIn[1].value = 1.5
        sumNode_2.portsIn[0].value = 2.0
        sumNode_2.portsIn[1].value = 2.25

        sumNode_3.evaluate()
        self.assertEqual(sumNode_3.portsOut[0].value, 6.75, "Output from Node 3 incorrect")

        # adding a forth node to the end of the fork
        sumNode_2.portsIn[0].value = 3.0
        negNode = graph.createNode(mNode.NegateNode)
        edgeCreated = sumNode_3.getOutputPort("result").connect(negNode.getInputPort("value"))
        self.assertTrue(edgeCreated)
        negNode.evaluate()
        self.assertEqual(negNode.portsOut[0].value, -7.75, "Output from Negate Node incorrect")

    def test_multipleOutputs(self):
        """
        Testing the

                      -- |Node|
                    /
            |Node|--
                    \
                      -- |Node|
        """
        graph = mGraph.Graph()
        negNode = graph.createNode(mNode.NegateNode)
        sumNode1 = graph.createNode(mNode.SumNode)
        sumNode2 = graph.createNode(mNode.SumNode)

        negNode.getOutputPort("result").connect(sumNode1.getInputPort("value1"))
        negNode.getOutputPort("result").connect(sumNode2.getInputPort("value1"))

        negNode.getInputPort("value").value = 1
        sumNode1.getInputPort("value2").value = 1
        sumNode2.getInputPort("value2").value = -1

        sumNode1.evaluate()
        sumNode2.evaluate()

        self.assertEqual(sumNode1.getOutputPort("result").value, 0)
        self.assertEqual(sumNode2.getOutputPort("result").value, -2)

    def test_disconnectNode(self):
        """
        Copy of "test_3NodeFork", except we disconnect Node2, and make sure that it doesn't get evaluated

        |node_1|--
                   \
                     --> |sumNode_3| --> |negateNode|
                   /
        |node_2|--

        """
        graph = mGraph.Graph()
        sumNode_1 = graph.createNode(mNode.SumNode)
        sumNode_2 = graph.createNode(mNode.SumNode)
        sumNode_3 = graph.createNode(mNode.SumNode)

        sumNode_1.getOutputPort("result").connect(sumNode_3.getInputPort("value1"))
        sumNode_2.getOutputPort("result").connect(sumNode_3.getInputPort("value2"))

        sumNode_1.portsIn[0].value = 1.0
        sumNode_1.portsIn[1].value = 1.5
        sumNode_2.portsIn[1].value = 2.25
        sumNode_2.portsIn[0].value = 3.0
        negNode = graph.createNode(mNode.NegateNode)
        sumNode_3.getOutputPort("result").connect(negNode.getInputPort("value"))
        negNode.evaluate()
        self.assertEqual(negNode.portsOut[0].value, -7.75, "Output from Negate Node incorrect")

        sumNode_2.getOutputPort("result").disconnect(sumNode_3.getInputPort("value2"))
        self.assertFalse(sumNode_2.getOutputPort("result").isConnected())
        self.assertFalse(sumNode_3.getInputPort("value2").isConnected())

        negNode.evaluate()
        self.assertEqual(negNode.portsOut[0].value, -2.5, "Output from Negate Node incorrect")


if __name__ == "__main__":
    unittest.main()