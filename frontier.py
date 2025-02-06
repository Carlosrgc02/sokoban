from bisect import insort

class Frontier:
    """
    ********************************************************************
    *
    * Class name: Frontier
    *
    * Name of the original author: Carlos Ruiz García-Casarrios
    *
    * Description of the class: The Frontier class implements a priority queue
    * that manages nodes in the search process. It provides methods for adding
    * nodes, popping nodes based on different strategies (BFS, DFS, UC), and
    * checking if the frontier is empty.
    *
    * Required Files: bisect (for maintaining sorted order in the frontier)
    *
    *********************************************************************
    """
    def __init__(self):
        """
        ********************************************************************
        *
        * Method name: __init__
        *
        * Description: Initializes the Frontier object with an empty list
        * to hold nodes.
        *
        *********************************************************************
        """
        self.nodes = []  # List that will hold the nodes in the frontier

    def pop(self, strategy):
        """
        ********************************************************************
        *
        * Method name: pop
        *
        * Description: Pops a node from the frontier based on the chosen
        * strategy. Currently, all strategies pop from the front.
        *
        * Calling arguments:
        * - strategy: The strategy to use when popping the node.
        *
        * Return value: The node that was popped, or None if the frontier is empty.
        *********************************************************************
        """
        if self.nodes:
            return self.nodes.pop(0)  # Always pop from the front
        return None

    def add(self, node):
        """
        ********************************************************************
        *
        * Method name: add
        *
        * Description: Adds a node to the frontier while maintaining the list
        * in sorted order. The sorting is first by the 'value' of the node,
        * and if there are ties, by the 'node_id'.
        *
        * Calling arguments:
        * - node: The node to add to the frontier.
        *
        * Return value: None (The node is added in place).
        *********************************************************************
        """
        # Insert the node into its correct position in the sorted list
        insort(self.nodes, node, key=lambda x: (x.value, x.node_id))

    def is_empty(self):
        """
        ********************************************************************
        *
        * Method name: is_empty
        *
        * Description: Checks if the frontier is empty.
        *
        * Return value: True if the frontier is empty, False otherwise.
        *********************************************************************
        """
        return len(self.nodes) == 0  # Returns True if the frontier is empty


    def __repr__(self):
        return f"Frontier(nodes={self.nodes})"
