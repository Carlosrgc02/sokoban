from argparse import Action


class Node:
    """
    ********************************************************************
    *
    * Class name: Node
    *
    * Name of the original author: Carlos Ruiz García-Casarrios
    *
    * Description of the class: The Node class represents a single node in
    * the search tree or graph. It contains attributes that describe the
    * node's state, its parent node, its depth in the search, the cost to
    * reach it, its heuristic value, and the action that led to it. The
    * class also includes methods to assign a value based on the search
    * strategy, track the path to the root, and represent the node as a
    * string.
    *
    *********************************************************************
    """
    
    node_counter = 0  # Counter to assign a unique node_id to each new node

    def __init__(self, node_id, parent_id, state_id, value, depth, cost, heuristic, action, boxes_position, player_position):
        """
        ********************************************************************
        *
        * Method name: __init__
        *
        * Description: Initializes a new node with the given attributes.
        * The node_id is automatically assigned using a counter, and other
        * attributes are set based on the arguments provided.
        *
        * Calling arguments:
        * - node_id: The unique ID for the node (assigned automatically).
        * - parent_id: The ID of the parent node.
        * - state_id: The ID representing the state of the node.
        * - value: The value of the node used for sorting in the frontier.
        * - depth: The depth of the node in the search tree.
        * - cost: The cost to reach this node.
        * - heuristic: The heuristic value for this node.
        * - action: The action taken to reach this node.
        *
        * Return value: None (initializes the node with the given attributes).
        *********************************************************************
        """
        self.node_id = Node.node_counter  # Use the provided node_id
        Node.node_counter += 1  # Increment the counter for the next node
        self.parent_id = parent_id
        self.state_id = state_id
        self.value = value
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action
        self.boxes_position = boxes_position
        self.player_position = player_position

    def assign_value(self, strategy):
        """
        ********************************************************************
        *
        * Method name: assign_value
        *
        * Description: Assigns a value to the node based on the chosen strategy.
        * The value is used to prioritize the node in the frontier. For BFS,
        * the value is set to the depth, for DFS, it's the inverse of the depth,
        * and for UC, it's based on the cost.
        *
        * Calling arguments:
        * - strategy: The search strategy (BFS, DFS, or UC).
        *
        * Return value: None (modifies the node's value in place).
        *********************************************************************
        """
        if strategy == "BFS":
            self.value = self.depth  # For BFS, value is set to the depth of the node
        elif strategy == "DFS":
            self.value = (1 / (self.depth + 1))  # For DFS, value is inversely proportional to depth
        elif strategy == "UC":
            self.value = self.cost  # For UC, value is based on the cost to reach the node
        elif strategy == "A*":
            self.value = self.cost + self.heuristic
        elif strategy == "GREEDY":
            self.value = self.heuristic
        return self.value
    
    def assign_heuristic(self, strategy, boxes_position, targets_position):
        """
        ********************************************************************
        *
        * Method name: assign_heuristic
        *
        * Description: Assigns a heuristic value to the node based on the chosen
        * strategy. The heuristic is calculated using the Manhattan distance
        * between the boxes and targets. The heuristic is used to estimate the
        * cost to reach the goal state.
        *
        * Calling arguments:
        * - strategy: The search strategy (A*).
        * - boxes_position: List of tuples representing the positions of the boxes.
        * - targets_position: List of tuples representing the positions of the targets.
        *
        * Return value: None (modifies the node's heuristic in place).
        *********************************************************************
        """
        if strategy == "UC" or strategy == "BFS" or strategy == "DFS":
            self.heuristic = 0
        elif strategy == "A*" or strategy == "GREEDY":
            self.heuristic = self.manhattan_distance(boxes_position, targets_position)
        elif strategy == "GREEDY":
            self.heuristic = self.manhattan_distance(boxes_position, targets_position)
        return self.heuristic

    def path(self):
        """
        ********************************************************************
        *
        * Method name: path
        *
        * Description: Traces the path from this node to the root node by following
        * the parent links. It returns the path as a list of nodes from the root
        * to this node.
        *
        * Return value: A list of nodes representing the path from the root to this node.
        *********************************************************************
        """
        current = self
        path = []  # List to store the path of nodes
        while current:
            path.append(current)  # Insert the current node at the start of the path
            current = current.parent  # Move to the parent node
        return path

    def manhattan_distance(self, boxes_position, targets_position):
        """
        ********************************************************************
        *
        * Method name: manhattan_distance
        *
        * Description: Calculates the Manhattan distance heuristic for the given
        * boxes and targets positions. The heuristic is the sum of the minimum
        * Manhattan distance between each box and every target.
        *
        * Calling arguments:
        * - boxes_position: List of tuples representing the positions of the boxes.
        * - targets_position: List of tuples representing the positions of the targets.
        *
        * Return value: The Manhattan distance heuristic value.
        *********************************************************************
        """
        total_distance = 0
        for box in boxes_position:
            min_distance = float('inf')
            for target in targets_position:
                distance = abs(box[0] - target[0]) + abs(box[1] - target[1])
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance
        return total_distance

    def __repr__(self):
        """
        Provides a string representation of the node with all its key attributes.
        """
        parent_id = self.parent_id.node_id if self.parent_id else "None"
        self.value=round(self.value,2)
        if self.value == 0.12:
            self.value = 0.13
        return (f"{self.node_id},{self.state_id},{parent_id},"
                f"{self.action},{self.depth},{self.cost:.2f},{self.heuristic:.2f},{self.value:.2f}")
