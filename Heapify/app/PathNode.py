"""
@author: Josiah Cherbony
@date: December 2022

This file contains a class for a PathNode which contains attributes for the path it contains,
the node to its left, right, generation_right, and parent. (these can be None) And
whether or not the node is the end of a level or the last node in the tree
"""

class PathNode():
    """
    PathNode class can create a node that contains a path, left, right, parent,
    and generation_right pointers. It also contains values if the node is the
    last node in a level or the last node in the tree.
    """

    def __init__(self, path, parent = None):
        """
        Creates a new PathNode object with a path, parent, left, right,
        generation_right, level end, and is last node instance. Level end,
        last node, left, and right are initially set to None.

        Args:
            path (Str): The path for the node to contain
            parent (PathNode): Optional, the parent of the node being created,
                               the value if not passed in is None
        """
        self.path = path
        self.left = None
        self.right = None
        self.parent = parent
        self.generation_right = None
        self.is_level_end = False
        self.is_last_node = False

    def swap_left(self, other):
        """
        Begins the swap of the self node with its left child

        Args:
            other (PathNode): The node to swap with
        """
        orginial_right = self.right
        self.left, other.left = other.left, self
        self.right, other.right = other.right, orginial_right
        self.swap_rest(other)

    def swap_right(self, other):
        """
        Begins the swap of the self node with its right child

        Args:
            other (PathNode): The node to swap with
        """
        orginial_left = self.left
        self.right, other.right = other.right, self
        self.left, other.left = other.left, orginial_left
        self.swap_rest(other)
        
    def swap_rest(self, other):
        """
        Finishes swapping two nodes by taking care of the exchange of parents,
        left, right, is level end, and is last node values.

        Args:
            other (PathNode): The node to switch with
        """
        # problem with new parents lefts and rights
        original_parent = self.parent
        self.parent, other.parent = other, original_parent

        # fix parents lefts and rights
        if original_parent:
            if original_parent.right == self:
                original_parent.right = other
            elif original_parent.left == self:
                original_parent.left = other
            
        # reconnect lower parent
        if self.left:
            self.left.parent = other
        if self.right:
            self.right.parent = other
        
        # fix generation right pointers and swap level end and last node value
        self.generation_right, other.generation_right = other.generation_right, self.generation_right
        self.is_level_end, other.is_level_end = other.is_level_end, self.is_level_end
        self.is_last_node, other.is_last_node = other.is_last_node, self.is_last_node

    def __str__(self):
        """
        Gives a string representation of the node

        Return:
            The string representation of the node ex. "1(0, 2)"
        """
        return '"' + str(len(self.path) - 1) + "(" + ", ".join(self.path) + ')"'

    def __eq__(self, other):
        """
        Checks equality of two nodes with their paths

        Args:
            other (PathNode): The node to compare with

        Return:
            True if the paths are the same, False otherwise
        """
        return self.path == other.path
    
    def __lt__(self, other):
        """
        Check if the node is less than another node with their paths

        Args:
            other (PathNode): The node to compare with

        Return:
            True if the path is less than other, False otherwise
        """
        return len(self.path) < len(other.path)

    def __gt__(self, other):
        """
        Check if the node is greater than another node with their paths

        Args:
            other (PathNode): The node to compare with

        Return:
            True if the path is greater than other, False otherwise
        """
        return len(self.path) > len(other.path)

    def __le__(self, other):
        """
        Check if the node is less than or equal to another node with their paths

        Args:
            other (PathNode): The node to compare with

        Return:
            True if the path is less than or equal to other, False otherwise
        """
        if len(self.path) == len(other.path):
            return True
        else:
            return len(self.path) < len(other.path)

    def __ge__(self, other):
        """
        Check if the node is greater than or equal to another node with their paths

        Args:
            other (PathNode): The node to compare with

        Return:
            True if the path is greater than or equal to other, False otherwise
        """
        if len(self.path) == len(other.path):
            return True
        else:
            return len(self.path) > len(other.path)