"""
@author: Josiah Cherbony
@date: December 2022

This file will read input from a command line argument and transform the input
into PathNodes to be put into a complete binary tree. It will also heapify the 
complete binary tree to transform it into a minheap. There are multiple methods 
for reading input, building the tree, heapifying, and printing out the original 
and heapified binary tree. The program will create files of the tree for before 
and after heapification. They will be .dot files and they will be able to be 
viewed as a .png file using graphviz.
"""

# import PathNode so the Nodes can be created from the input command line arg.
from PathNode import PathNode

class Heap():
    """
    Heap class can create nodes from an input file and use those nodes to build a
    complete binary tree. The tree can set the level ends, last node, and 
    generation links. The tree can be printed and heapified and the go function
    allows the driver to create .dot files to be viewed as a .png in graphviz.
    """

    def __init__(self, input_file, label):
        """
        Creates a heap opject with an input file, list to hold its contents, root, label,
        and message for printing. root and message are initialize to None at first.

        args:
            input_file (str): the file to create nodes from (command line argument)
            label (str): the label to give to the .dot files (command line argument)
        """
        # start at 0 to make creating the nodes easier
        self.temp_path = [0]
        self.input_file = input_file
        self.root = None
        self.label = label
        self.msg = None

    def read_paths(self, input_file):
        """
        Reads the contents of the files as paths for the PathNodes by adding each line
        of the file to the temp_path attribute. 

        args:
            input_file (str): The file to read from
        
        raise:
            ValueError if an input contains a node with an empty path
        """
        with open(input_file) as file:
            # iterate through the lines of the file
            for line in file:
                line = line.strip().split()
                # If we're given a node with an empty path 
                if(line == ["0"]):
                    raise ValueError("\nError! Input can't contain node with empty path.\n")
                # add the acceptable line to temp_path
                self.temp_path.append(line)

    def build_complete_tree(self, index, parent=None):
        """
        Takes the paths in temp_path and creates PathNodes from them. Also creates a
        complete binary tree from the nodes in the order of which they are created.
        Nodes are added left to right recursively.

        args:
            index (int): The index for temp_path to get the value we want
            parent (PathNode): The node to be the parent of the next node(s) added to the tree.
                               The default value for parent is None.
            
        returns:
            path_node (PathNode): the PathNode createc.
        """
        path_node = None
        
        # keep the index inbounds for recursive calls
        if index < len(self.temp_path):

            # make a node with the appropriate parent, None if root
            path_node = PathNode(self.temp_path[index], parent)

            # set the root of the tree and set the last node of the tree
            if index == 1: self.root = path_node
            if index == len(self.temp_path) - 1: path_node.is_last_node = True 

            # make the left/right nodes of the current node in the tree
            path_node.left = self.build_complete_tree(2 * index, path_node)
            path_node.right = self.build_complete_tree(2 * index + 1, path_node)
        
        return path_node

    def set_level_end(self, root):
        """
        Sets the nodes that end the level for the binary tree recursively.

        Args:
            root (PathNode): The node that we are currently at.
        """
        if root:
            # set level end and move to only right nodes recursively
            root.is_level_end = True 
            self.set_level_end(root.right)

    def set_generation_links(self, root):
        """
        Sets the generation links for the nodes in the tree (generation_right)
        by connecting roots with 2 children and connecting the right childs
        generation right to the left child of the roots generation right node

        args:
            root (PathNode): The PathNode we are currently at. 
        """
        if root and root.left and root.right:

            # connect nodes that dont share a parent
            if root.right and root.generation_right:
                root.right.generation_right = root.generation_right.left

            # connect children that share a parent
            root.left.generation_right = root.right

            # traverse the rest of the tree
            self.set_generation_links(root.left)
            self.set_generation_links(root.right)

    def print_tree_levels(self, root, before):
        """
        Creates the tree levels in the format to be put into the .dot files for graphviz
        does this level by level and uses the helper method print_tree_level
        to do so.

        Args:
            root (PathNode): The PathNode we are currently at.
            before (int): Our index for print tree levels (node "index")
        """
        index = 0
        # Reseting the msg to get the current tree
        if before:
            self.msg = "digraph " + self.label + "Before{\n"
        else:
            self.msg = "digraph " + self.label + "After{\n"
        # Traverse all nodes with a level
        while root.left:
            index = self.print_tree_level(root, index)
            root = root.left
        # account for last level
        index = self.print_tree_level(root, index)
        self.print_paths(0, 1, index - 1)
        # add closing bracket to the very end
        self.msg += '}'
        
    def print_tree_level(self, node, index):
        """
        Makes the message for the graphviz .dot file of a single level in the tree

        Args:
            node (PathNode): The node we are currently at
            index (int): The "index" of the node we are currently at (what number it is)

        Return:
            index (int): The new index we are at after traversing the level and incrementing it
        """
        # traverse all nodes in level
        while node.generation_right:
            # add node in format and move to next
            self.msg += '\t' + str(index) + '[label=' + node.__str__() + '];\n'
            node = node.generation_right
            index += 1
        # account for last level
        self.msg += '\t' + str(index) + '[label=' + node.__str__() + '];\n' 
        index += 1
        return index

    def print_paths(self, index, next_node, stop_point):
        """
        Adds the paths (pointers) of each node at the bottom of our .dot graphviz file
        and adds the paths recursively
        ex. let 0 be the root and 1 its left and 2 its right,
        0 -> 1
        0 -> 2, etc.

        Args:
            index (int): The number ordering of the node we are at
            next_node (int): The next node index
            stop_point (int): The node index to stop at
        """
        # stay in bounds of # of nodes
        if next_node <= stop_point:
            # determine left and right nodes
            if next_node % 2 == 1:
                self.msg = self.msg + "\t" + str(index) + " -> " + str(next_node) + ";\n"
                self.print_paths(index, next_node + 1, stop_point)
            elif next_node % 2 == 0:
                self.msg = self.msg + "\t" + str(index) + " -> " + str(next_node) + ";\n"
                self.print_paths(index + 1, next_node + 1, stop_point)

    def heapify(self, root):
        """
        Heapifys the complete binary tree by going to the last node with children,
        swapping if necessary, moving to the preceding node, and repeating.
        Makes a minheap, and traverses nodes recursively.

        args:
            root (PathNode): The PathNode to start at
        """
        if root:
            
            # cannot heapify a leaf
            if not self.leaf(root):

                # get to left most node on the level of the last node with children
                if root.left and not self.leaf(root.left):
                    self.heapify(root.left)

                # move right to the last node with children
                if root.generation_right and not self.leaf(root.generation_right):
                    self.heapify(root.generation_right)
                
                # see if a swap needs to be made and make it if it does
                self.check_swap(root, root.left, root.right)

    def check_swap(self, root, root_left, root_right):
        """
        Checks if a swap needs to be made by sending the right case to the appropriate
        swap helper function, ex. 2 children, only left, only right.

        Args:
            root (PathNode): The node we are at
            root_left (PathNode): The left child from root (can be None)
            root_right (PathNode): The right child from root (can be None)
        """
        # check for swap if root has 2 children
        if root_left and root_right:
            self.double_swap(root, root_left, root_right)

        # check for a left swap if the leaf only has left child
        if root_left and not root_right:
            self.left_swap(root, root_left)

        # check for a right swap if the leaf only has right child
        if root_right and not root_left:
            self.right_swap(root, root_right)

    def double_swap(self, root, root_left, root_right):
        """
        If the root has 2 children then if left is smaller than right, swap root with left,
        if right is smaller than left, swap root right, if children are equal then swap
        with left.

        Args:
            root (PathNode): The node we are at
            root_left (PathNode): The left child from root (can be None)
            root_right (PathNode): The right child from root (can be None)
        """
        # check for left swap if left child is smaller than right
        if root_left < root_right:
            self.left_swap(root, root_left)

        # check for right swap if right child is smaller than left
        elif root_left > root_right:
            self.right_swap(root, root_right)

        # check for left swap if both children are the same length
        else: 
            self.left_swap(root, root_left)

    def right_swap(self, root, root_right):
        """
        If the right child is smaller than the root and not the same size as the root
        make the swap with right child.

        Args:
            root (PathNode): The node we are at
            root_right (PathNode): The right child from root (can be None)
        """
        # check if the child is smaller and not the same size of the root
        if root_right < root and (not root_right >= root): 
                
            # handle a change of root and make right swap
            if self.is_root(root): self.root = root_right
            root.swap_right(root_right)

    def left_swap(self, root, root_left):
        """
        If the left child is smaller than the root and not the same size as the root
        make a swap with left child.

        Args:
            root (PathNode): The node we are at
            root_left (PathNode): The left child from root (can be None)
        """
        # check if the child is smaller and not the same size of the root
        if root_left < root and (not root_left >= root): 
            
            # handle a change of root and make left swap
            if self.is_root(root): self.root = root_left
            root.swap_left(root_left)

    def is_heap(self, root):
        """
        Checks if the tree is a complete heap by making sure no root has children
        smaller than itself, traverses tree recursively.

        Args:
            root (PathNode): The node we are at

        Return:
            boolean: True if tree is a heap, False otherwise
        """
        # check if the tree is a heap and needs to heapify again
        if not self.leaf(root):
            # if only left child
            if root.left and not root.right:
                return root <= root.left
            # if left and right child
            elif root.left and root.right:
                # check root is smaller than children and traverse if it is
                if root <= root.left and root <= root.right:
                    return self.is_heap(root.left) and self.is_heap(root.right)
                else:
                    return False
        else:
            return True

    def is_root(self, root):
        """
        Checks if the node we are at is the root of the entire tree

        Args:
            root (PathNode): The node we are currently at
        """
        return root.parent is None

    def leaf(self, root):
        """
        Checks if the node we are at is a leaf

        Args:
            root (PathNode): The node we are currently at
        """
        return root.left is None and root.right is None

    def go(self):
        """
        Acts a starting point for the Heap to be called in the driver, reads the file input,
        builds and sets binary tree, makes the before file for graphviz, heapifys,
        and makes the after file for graphviz.
        """
        # read input
        self.read_paths(self.input_file)
    
        # build tree
        self.build_complete_tree(1)
        self.set_level_end(self.root)
        self.set_generation_links(self.root)
        
        # make the .dot file for graphviz (not heapified)
        self.print_tree_levels(self.root, True)
        with open(self.label + "Before.dot", "w") as file:
            file.write(self.msg)
        print(self.msg)
        print()

        #heapify
        while not self.is_heap(self.root):
            self.heapify(self.root)
            # make sure the links always hold up if we heapify more than once
            self.set_generation_links(self.root)

        # make the .dot file for graphviz (heapified)
        self.print_tree_levels(self.root, False)
        with open(self.label + "After.dot", "w") as file:
            file.write(self.msg)
        print(self.msg)
