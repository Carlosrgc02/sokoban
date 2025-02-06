#!/usr/bin/python3

import argparse
import sys
import re
import hashlib

from node import Node
from frontier import Frontier
from visited_states import VisitedStates
from collections import deque

class Sokoban:
    """
    *********************************************************************
    *
    * Class Name: Sokoban
    * Author/s name: Carlos Ruiz Garcia-Casarrubios
    * Release/Creation date: 05/10/24
    * Class version: 3.0
    * Class description: Main class of the sokoban laboratory project where we print the id, number
    * of rows, columns, the position of the walls, targets, player and boxes to the user.
    *
    **********************************************************************
    """
    targets_position = []
    def __init__(self, level_string):
        """
        ********************************************************************
        *
        * Method name: __init__
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Initializes the Sokoban game level, parsing the level
        * to extract rows, columns, walls, targets, player, and boxes positions.
        * Calling arguments: level_string (str)
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        self.level_string = level_string.replace('\\n', '\n')
        self.rows = self.count_rows()
        self.columns = self.count_columns()
        self.matrix = self.create_level_matrix()
        self.get_level_assets()
        self.level_id = self.generate_level_id(self.player_position, self.boxes_position)

    def get_level_assets(self):
        """
        ********************************************************************
        *
        * Method name: get_level_assets
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Collects all asset positions in a single pass
        * through the level matrix.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        self.walls_position = []
        Sokoban.targets_position = []
        self.player_position = None
        self.boxes_position = []
        self.boxes_pos_aux = []
        self.box_target_position = []

        for i, row in enumerate(self.matrix):
            for j, element in enumerate(row):
                if element == '#':
                    self.walls_position.append((i, j))
                if element in ['.', '*']:
                    Sokoban.targets_position.append((i, j))
                if element in ['@', '+']:
                    self.player_position = (i, j)
                if element in ['$', '*']:
                    self.boxes_position.append((i, j))
                if element == '$':
                    self.boxes_pos_aux.append((i, j))
                if element == '*':
                    self.box_target_position.append((i, j))

    @staticmethod
    def args_parse():
        """
        ********************************************************************
        *
        * Method name: args_parse
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Parsing of the command line arguments to check and manipulate them
        * Calling arguments: none 
        * Return value: parser
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('action')
        parser.add_argument('-l', '-level', type=str, required=True)
        parser.add_argument('-s', type=str, help='Strategy for T3 (BFS, DFS, UC, A*, GREEDY)')
        parser.add_argument('-d', type=int, help='Maximum depth for T3')
        return parser.parse_args()

    def count_rows(self):
        """
        ********************************************************************
        *
        * Method name: count_rows
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Method to count the rows of a level 
        * Return value: int rows
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """   
        return len(self.level_string.split('\n'))

    def count_columns(self):
        """
        ********************************************************************
        *
        * Method name: count_columns
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Method to count the columns of a level 
        * Return value: int first_line 
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """ 
        return max(len(line) for line in self.level_string.split('\n'))

    def create_level_matrix(self):
        """
        ********************************************************************
        *
        * Method name: create_level_matrix
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Conversion of the level string into a char matrix for further manipulation
        * of the level
        * Return value: matrix[]
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """   
        return [list(line) for line in self.level_string.split('\n')]

    def generate_level_id(self, player_position, boxes_position):
        """
        ********************************************************************
        *
        * Method name: generate_level_id
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Generates a unique level identifier
        * based on the player's current position and the positions of the boxes.
        * The identifier is created by formatting the player and box positions
        * and converting it to an MD5 hash.
        * Return value: MD5 hash string representing the level ID.
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        level_id_str = f"({player_position[0]},{player_position[1]})" + "[" + ",".join(f"({i},{j})" for i, j in boxes_position) + "]"
        return self.id_md5(level_id_str)

    def id_md5(self, id_str):
        """
        ********************************************************************
        *
        * Method name: id_md5
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Conversion of the id to md5
        * Return value: id string
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """   
        md5 = hashlib.md5()
        md5.update(id_str.encode('utf-8'))
        return md5.hexdigest().upper()

    def display_level_info(self):
        """
        ********************************************************************
        *
        * Method name: display_level_info
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Displays the current level information,
        * including the level ID (computed as an MD5 hash), dimensions of the
        * level, positions of walls, targets, player, and boxes. This method
        * formats the output for clarity and readability.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        print(f"ID:{self.level_id}")
        print(f"Rows:{self.rows}")
        print(f"Columns:{self.columns}")
        print(f"Walls:[{','.join(f'({i},{j})' for i, j in self.walls_position)}]")
        print(f"Targets:[{','.join(f'({i},{j})' for i, j in self.targets_position)}]")
        print(f"Player:({self.player_position[0]},{self.player_position[1]})")
        print(f"Boxes:[{','.join(f'({i},{j})' for i, j in self.boxes_position)}]")

   

    def is_goal_state(self, boxes_position):
        """
        ********************************************************************
        *
        * Method name: is_goal_state
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Checks if all boxes are positioned on
        * their respective target positions, indicating a goal state.
        * Return value: True if all boxes are on targets, False otherwise.
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        return all(pos in Sokoban.targets_position for pos in boxes_position)


        
    def search_algorithm(self, initial_node, strategy, max_depth):
        """
        ********************************************************************
        *
        * Method name: search_algorithm
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the search algorithm to solve
        * the Sokoban level using the specified strategy and maximum depth.
        * The method initializes the frontier, visited states, and solution
        * variables, adding the initial node to the frontier. It then iterates
        * through the frontier, expanding nodes and generating successors until
        * a solution is found or the frontier is empty.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        visited = VisitedStates()
        solution = False
        frontier = Frontier()
        initial_node.assign_heuristic(strategy, self.boxes_position, Sokoban.targets_position)
        initial_node.assign_value(strategy)
        frontier.add(initial_node)
        print(initial_node)
        
        while not frontier.is_empty():
            node = frontier.pop(strategy)  # Pop from the front for all strategies
            if self.is_goal_state(node.boxes_position):
                solution = True
                break
            else:
                if node.depth < max_depth:
                    if not visited.is_visited(node.state_id):
                        visited.add_state(node.state_id)
                        successors = self.generate_succesors(node.player_position, node.boxes_position)
                        for action, new_state, cost, new_player_pos, new_boxes_pos in successors:
                            new_node = Node(node.node_id, node, new_state, 0, node.depth + 1, node.cost + cost, 0.00, action, new_boxes_pos, new_player_pos)
                            new_node.assign_heuristic(strategy, new_boxes_pos, Sokoban.targets_position)
                            new_node.assign_value(strategy)
                            frontier.add(new_node)
        
        path = deque()
        if solution:
            while node.parent_id is not None:
                path.appendleft(node)
                node = node.parent_id

            for n in path:
                print(n)
        else:
            print("NO SOLUTION")
        
    def generate_succesors(self, plr_position, boxs_position):
        """
        ********************************************************************
        *
        * Method name: execute_T2S
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the T2S action to generate
        * all possible successor states from the current game state based
        * on player movements and box pushes. It considers the player's
        * position, walls, and boxes to determine valid actions, storing
        * the resulting states and their corresponding level IDs.
        * Return value: List of ordered successors, where each successor
        * is represented as a tuple containing the action, new level ID,
        * and cost.
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        directions = {
            'u': (-1, 0), 'r': (0, 1), 'd': (1, 0), 'l': (0, -1),
            'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)
        }
        successors = []
        cost = 1
        
        for action, (di, dj) in directions.items():
            new_player_pos = (plr_position[0] + di, plr_position[1] + dj)
            
            if action.islower() and Sokoban.is_valid_position(new_player_pos, self.walls_position, boxs_position):
                new_level_id = self.generate_level_id(new_player_pos, boxs_position)
                successors.append((action, new_level_id, cost, new_player_pos, boxs_position))

            elif action.isupper():
                box_pos = new_player_pos
                new_box_pos = (box_pos[0] + di, box_pos[1] + dj)

                if box_pos in boxs_position and Sokoban.can_push_box(box_pos, (di, dj), self.walls_position, boxs_position):
                    new_boxes_pos = sorted([pos if pos != box_pos else new_box_pos for pos in boxs_position])
                    new_level_id = self.generate_level_id(new_player_pos, new_boxes_pos)
                    successors.append((action, new_level_id, cost, new_player_pos, new_boxes_pos))

        ordered_successors = sorted(successors, key=lambda x: 'uUrRdDlL'.index(x[0]))
        return ordered_successors

    
    def print_successors(self, successors):
        """
        ********************************************************************
        *
        * Method name: print_successors
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Prints all the successors generated by
        * the T2S action. Each successor is displayed with its associated action,
        * new level ID, and the cost of the action.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        print(f"ID:{self.level_id}")
        for action, new_level_id, cost, _, _ in successors:
            print(f"[{action},{new_level_id},{cost}]")

    def level_checker(self):
        """
        ********************************************************************
        *
        * Method name: level_checker
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Checking of the command line arguments to match expected chars
        * Calling arguments: level string args 
        * Return value: boolean 
        * Required Files: none
        * List of Checked Exceptions: ValueError for correct level input
        *********************************************************************
        """
        allowed_chars = r'^[#@$.*+ \n]+$'
        if not re.fullmatch(allowed_chars, self.level_string):
            raise ValueError("Introduced level contains not valid characters")

    @staticmethod
    def print_matrix(matrix):
        """
        ********************************************************************
        *
        * Method name: print_matrix
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Prints the game matrix in a formatted
        * way, displaying each element within square brackets for clarity.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        for row in matrix:
            formatted_row = [repr(elem) for elem in row]
            print(f"[{', '.join(formatted_row)}]")

    @staticmethod
    def validate_t3_args(args):
        """
        ********************************************************************
        *
        * Method name: validate_t3_args
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Validates the arguments provided for
        * the T3 action, specifically checking if the strategy and maximum
        * depth parameters are correctly specified. The function checks that
        * the strategy is one of the valid values ("BFS", "DFS", "UC", "A*", "GREEDY") and
        * that the maximum depth is an integer.
        * Calling arguments: args (Namespace) - parsed command-line arguments
        * Return value: A tuple containing the strategy (str) and maximum depth (int)
        * Required Files: none
        * List of Checked Exceptions: sys.exit() in case of invalid input
        *********************************************************************
        """
        # Check if both strategy (-s) and maximum depth (-d) are provided
        if not args.s or not args.d:
            print("Error: You must specify -s (strategy) and -d (maximum depth) parameters for T3.")
            sys.exit(1)  # Exit the program if any argument is missing
        
        # Convert the strategy to uppercase and validate it
        strategy = str(args.s.upper())
        if strategy not in ["BFS", "DFS", "UC", "A*", "GREEDY"]:
            print(f"Error: Strategy {strategy} is not valid. Choose BFS, DFS, UC, A*, or GREEDY.")
            sys.exit(1)  # Exit if the strategy is not one of the valid options
        
        # Try to convert the maximum depth to an integer
        try:
            max_depth = int(args.d)
        except ValueError:
            print("Error: Maximum depth must be an integer.")
            sys.exit(1)  # Exit if the maximum depth is not a valid integer

        # Return the validated strategy and maximum depth
        return strategy, max_depth

    @staticmethod
    def is_valid_position(position, walls, boxes):
        return position not in walls and position not in boxes

    @staticmethod
    def can_push_box(box_position, direction, walls, boxes):
        new_box_pos = (box_position[0] + direction[0], box_position[1] + direction[1])
        return new_box_pos not in walls and new_box_pos not in boxes
    
    def execute_T1(self):
        """
        ********************************************************************
        *
        * Method name: execute_T1
        *   
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the T1 action to display the
        * level information to the user. This method calls the display_level_info()
        * function to print the level ID, number of rows and columns, walls,
        * targets, player, and boxes to the console.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        self.display_level_info()
    
    def execute_T2S(self, node, strategy):
        """
        ********************************************************************
        *
        * Method name: execute_T2S
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the T2S action to generate
        * all possible successor states from the current game state based
        * on player movements and box pushes. It considers the player's
        * position, walls, and boxes to determine valid actions, storing
        * the resulting states and their corresponding level IDs.
        * Return value: List of ordered successors, where each successor
        * is represented as a tuple containing the action, new level ID,
        * and cost.
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        successors = self.generate_succesors(node.player_position, node.boxes_position)
        return successors
    
    def execute_T2T(self):
        """
        ********************************************************************
        *
        * Method name: execute_T2T
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the T2T action to check if
        * the current box positions match the target positions, indicating
        * a goal state. Prints "TRUE" if it is a goal state, otherwise
        * prints "FALSE".
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
       
        if self.is_goal_state(self.boxes_position):
            print("TRUE")
        else:
            print("FALSE")

    def execute_T3(self, strategy, max_depth): 
        """
        ********************************************************************
        *
        * Method name: execute_T3
        *
        * Name of the original author: Carlos Ruiz García-Casarrios
        *
        * Description of the Method: Executes the T3 action to solve the
        * Sokoban level using the specified search strategy and maximum depth.
        * The method initializes the search algorithm with the initial node
        * and the provided strategy and maximum depth.
        * Return value: None
        * Required Files: none
        * List of Checked Exceptions: none
        *********************************************************************
        """
        initial_node = Node(0, None, self.level_id, 0.00, 0, 0.00, 0.00, "NOTHING", self.boxes_position, self.player_position)
        self.search_algorithm(initial_node, strategy, max_depth)

def main():
    """
    ********************************************************************
    *
    * Method name: main
    *
    * Name of the original author: Carlos Ruiz García-Casarrios
    *
    * Description of the Method: The main function that drives the Sokoban
    * program. It parses command-line arguments, initializes the Sokoban
    * game with a level string, checks the validity of the level, and then
    * executes the corresponding action (T1, T2S, T2T, or T3) based on the
    * provided arguments.
    * Calling arguments: none (args are parsed via Sokoban.args_parse())
    * Return value: None
    * Required Files: sokoban.py (where the Sokoban class and methods are defined)
    * List of Checked Exceptions: ValueError (if the level is invalid)
    *********************************************************************
    """
    args = Sokoban.args_parse()  # Parse arguments
    sokoban = Sokoban(args.l)  # Initialize Sokoban with level string

    try:
        sokoban.level_checker()
    except ValueError as e:
        print(e)
        sys.exit(1)

    if args.action == 'T1':
        sokoban.execute_T1()
    elif args.action == 'T2S':
        player_position = sokoban.player_position
        successors = sokoban.generate_succesors(player_position, sokoban.boxes_position)
        sokoban.print_successors(successors)
    elif args.action == 'T2T':
        sokoban.execute_T2T()
    elif args.action == 'T3':
        print(args.l)
        strategy, max_depth = sokoban.validate_t3_args(args)
        sokoban.execute_T3(strategy, max_depth)
    else:
        print(f"Action '{args.action}' is not valid. Please choose a valid action.")

if __name__ == '__main__':
    main()
