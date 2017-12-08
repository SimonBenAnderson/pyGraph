
"""
PyGraph
Created: Simon Anderson


"""

import Node
reload(Node)
# main function
if __name__ == "__main__":
    print("Initialising pyGraph.")

    # CREATE NODE 1
    sumNode = Node.SumNode()
    sumNode.portsIn[0].value = 1.0
    port = sumNode.addInputPort()
    port.value = 2.4
    sumNode.evaluate()
    print("{} >> {}".format(sumNode, sumNode.portsOut[0].value))


    # CREATE NODE 2
    sumNode_2 = Node.SumNode()
    sumNode_2.portsIn[0].value = 2.0
    sumNode_2.portsIn[1].value = 2.0
    sumNode_2.evaluate()
    print("{} >> {}".format(sumNode_2, sumNode_2.portsOut[0].value))

    # CONNECT NODE 1+2
