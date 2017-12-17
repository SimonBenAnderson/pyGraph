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

    def test_SubtractNode(self):
        subNode = mNode.SubtractNode()
        subNode.portsIn[0].value = 20
        subNode.portsIn[1].value = 10
        subNode.evaluate()
        self.assertEqual(subNode.portsOut[0].value, 10)

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

    def test_MultipleOutputs(self):
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

        heads = graph.getNetworkHeads()
        self.assertEqual(len(heads), 2)
        tails = graph.getNetworkTails()
        self.assertEqual(len(tails), 1)

    def test_DisconnectNode(self):
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

        heads = graph.getNetworkHeads()
        self.assertEqual(len(heads), 1)
        tails = graph.getNetworkTails()
        self.assertEqual(len(tails), 2)

        sumNode_2.getOutputPort("result").disconnect(sumNode_3.getInputPort("value2"))
        self.assertFalse(sumNode_2.getOutputPort("result").isConnected())
        self.assertFalse(sumNode_3.getInputPort("value2").isConnected())
        self.assertEqual(sumNode_3.getInputPort("value2").value, 5.25, "Disconnected port values should be equal to there last connected input")

        negNode.evaluate()
        self.assertEqual(negNode.portsOut[0].value, -7.75, "Output from Negate Node incorrect")

        heads = graph.getNetworkHeads()
        self.assertEqual(len(heads), 2)

    def test_NodeIsConnected(self):
        """
        Creates 3 nodes, 2 connected one not, Checks the node isConnected method is working correctly
        [n] -- [n]
        [n]
        """
        graph = mGraph.Graph()
        nSum1 = graph.createNode(mNode.SumNode)
        nSum2 = graph.createNode(mNode.SumNode)
        nSum3 = graph.createNode(mNode.SumNode)

        nSum1.getOutputPort("result").connect(nSum2.getInputPort("value1"))

        self.assertFalse(nSum3.isConnected())
        self.assertTrue(nSum1.isConnected())
        self.assertTrue(nSum2.isConnected())

        # testing graph tail and head retrieval
        heads = graph.getNetworkHeads()
        self.assertEqual(len(heads),2)
        tails = graph.getNetworkTails()
        self.assertEqual(len(tails),2)

    def test_DirtyEvaluation(self):
        """
        This method tests to see if dirty nodes get evaluated, and clean nodes just get there values read.
        Trying to be more efficient with how nodes are evaluated and executed.

        Thought behind implementation:
            If there was a graph with a thousand interconnected nodes, and nothing was dirtied, but the graph needed to evaluate
            how can we keep the computations to a minimum

        """
        graph = mGraph.Graph()
        sumNode_1 = graph.createNode(mNode.SumNode)
        sumNode_2 = graph.createNode(mNode.SumNode)
        subNode = graph.createNode(mNode.SubtractNode)
        negNode = graph.createNode(mNode.NegateNode)

        sumNode_1.getOutputPort("result").connect(subNode.getInputPort("value1"))
        sumNode_2.getOutputPort("result").connect(subNode.getInputPort("value2"))
        subNode.getOutputPort("result").connect(negNode.getInputPort("value"))

        sumNode_1.portsIn[0].value = 1.0
        sumNode_1.portsIn[1].value = 1.25
        sumNode_2.portsIn[0].value = 3.0
        sumNode_2.portsIn[1].value = 2.25

        negNode.evaluate()
        self.assertEqual(negNode.getOutputPort("result").value, 3)

        sumNode_1.portsIn[0].value = 0.0
        graph.evaluate()
        self.assertEqual(negNode.getOutputPort("result").value, 4)


if __name__ == "__main__":
    unittest.main()