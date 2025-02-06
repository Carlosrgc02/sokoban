class VisitedStates:
    """
    ********************************************************************
    *
    * Class name: VisitedStates
    *
    * Name of the original author: Carlos Ruiz García-Casarrios
    *
    * Description of the class: The VisitedStates class is responsible for
    * tracking the states that have already been visited in the search process.
    * It uses a set to store the state IDs and provides methods to add new
    * states to the visited set and check if a particular state has been visited.
    *
    *********************************************************************
    """

    def __init__(self):
        """
        ********************************************************************
        *
        * Method name: __init__
        *
        * Description: Initializes an empty set called 'visited' to store state IDs
        * that have been visited during the search process.
        *
        * Calling arguments: None
        *
        * Return value: None (initializes the 'visited' set).
        *********************************************************************
        """
        self.visited = set()  # Create an empty set to store visited states

    def add_state(self, state_id):
        """
        ********************************************************************
        *
        * Method name: add_state
        *
        * Description: Adds a given state ID to the set of visited states.
        * This method is used to mark a state as visited once it has been processed.
        *
        * Calling arguments:
        * - state_id: The ID of the state to be added to the visited set.
        *
        * Return value: None (adds the state to the visited set).
        *********************************************************************
        """
        self.visited.add(state_id)  # Add the state ID to the visited set

    def is_visited(self, state_id):
        """
        ********************************************************************
        *
        * Method name: is_visited
        *
        * Description: Checks if a given state ID is present in the visited set.
        * This method is used to determine whether a state has already been processed.
        *
        * Calling arguments:
        * - state_id: The ID of the state to check.
        *
        * Return value:
        * - True if the state ID is in the visited set, False otherwise.
        *********************************************************************
        """
        return state_id in self.visited  # Return True if the state has been visited, False otherwise
