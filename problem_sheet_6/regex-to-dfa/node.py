class Node:
    """
    Base class for nodes in the regular expression parse tree.
    """

    firstpos = None
    lastpos = None
    nullable = None

    def __init__(self, parent):
        """
        Initializes a Node object with a parent node.
        """
        self.parent = parent

    def create_subtree(self, nodestack):
        """
        Creates a subtree for the current node by popping two nodes from the nodestack
        and adding them as left and right children of the current node.
        """
        pass

    def isnullable(self):
        """
        Checks if the node is nullable (can match an empty string).
        """
        pass

    def findfirstpos(self):
        """
        Finds the set of positions in the parse tree where the first occurrence of the node can be found.
        """
        pass

    def findlastpos(self):
        """
        Finds the set of positions in the parse tree where the last occurrence of the node can be found.
        """
        pass


class ConcatNode(Node):
    """
    Node class for concatenation operation in the regular expression parse tree.
    """

    def __init__(self, parent):
        """
        Initializes a ConcatNode object with a parent node.
        """
        super().__init__(parent)
        self.lchild = None
        self.rchild = None

    def create_subtree(self, nodestack):
        """
        Creates a subtree for the current ConcatNode by popping two nodes from the nodestack
        and adding them as left and right children of the current node.
        """
        operand2 = nodestack.pop()
        operand1 = nodestack.pop()

        # if the operand is a node, then add it as a child
        # else create a leaf node and add it as a child
        # isinstance() is used to check if the operand is a node
        if isinstance(operand1, Node):
            self.lchild = operand1
            operand1.parent = self
        else:
            self.lchild = LeafNode(parent=self, string=operand1)

        if isinstance(operand2, Node):
            self.rchild = operand2
            operand2.parent = self
        else:
            self.rchild = LeafNode(parent=self, string=operand2)

    def __str__(self):
        """
        Returns a string representation of the ConcatNode.
        """
        return '[' + str(self.lchild) + '.' + str(self.rchild) + ']'

    def isnullable(self):
        """
        Checks if the ConcatNode is nullable (can match an empty string).
        """
        a = self.lchild.isnullable()
        b = self.rchild.isnullable()
        self.nullable = a and b
        return self.nullable

    def findfirstpos(self):
        """
        Finds the set of positions in the parse tree where the first occurrence of the ConcatNode can be found.
        """
        a = self.lchild.findfirstpos()
        b = self.rchild.findfirstpos()
        if self.lchild.nullable:
            self.firstpos = list(set(a + b))
        else:
            self.firstpos = a
        return self.firstpos

    def findlastpos(self):
        """
        Finds the set of positions in the parse tree where the last occurrence of the ConcatNode can be found.
        """
        a = self.lchild.findlastpos()
        b = self.rchild.findlastpos()
        if self.rchild.nullable:
            self.lastpos = list(set(a + b))
        else:
            self.lastpos = b
        return self.lastpos


class StarNode(Node):
    """
    Node class for Kleene star operation in the regular expression parse tree.
    """

    def __init__(self, parent):
        """
        Initializes a StarNode object with a parent node.
        """
        super().__init__(parent)
        self.child = None

    def create_subtree(self, nodestack):
        """
        Creates a subtree for the current StarNode by popping a node from the nodestack
        and adding it as the child of the current node.
        """
        operand = nodestack.pop()
        if isinstance(operand, Node):
            self.child = operand
        else:
            self.child = LeafNode(parent=self, string=operand)

    def __str__(self):
        """
        Returns a string representation of the StarNode.
        """
        return '[ (' + str(self.child) + ') * ]'

    def isnullable(self):
        """
        Checks if the StarNode is nullable (can match an empty string).
        """
        self.child.isnullable()
        self.nullable = True
        return True

    def findfirstpos(self):
        """
        Finds the set of positions in the parse tree where the first occurrence of the StarNode can be found.
        """
        self.firstpos = self.child.findfirstpos()
        return self.firstpos

    def findlastpos(self):
        """
        Finds the set of positions in the parse tree where the last occurrence of the StarNode can be found.
        """
        self.lastpos = self.child.findlastpos()
        return self.lastpos


class OrNode(Node):
    """
    Node class for union operation in the regular expression parse tree.
    """

    def __init__(self, parent):
        """
        Initializes an OrNode object with a parent node.
        """
        super().__init__(parent)
        self.lchild = None
        self.rchild = None

    def create_subtree(self, nodestack):
        """
        Creates a subtree for the current OrNode by popping two nodes from the nodestack
        and adding them as left and right children of the current node.
        """
        operand2 = nodestack.pop()
        operand1 = nodestack.pop()

        if isinstance(operand1, Node):
            self.lchild = operand1
            operand1.parent = self
        else:
            self.lchild = LeafNode(parent=self, string=operand1)

        if isinstance(operand2, Node):
            self.rchild = operand2
            operand2.parent = self
        else:
            self.rchild = LeafNode(parent=self, string=operand2)

    def __str__(self):
        """
        Returns a string representation of the OrNode.
        """
        return '[' + str(self.lchild) + '|' + str(self.rchild) + ']'

    def isnullable(self):
        """
        Checks if the OrNode is nullable (can match an empty string).
        """
        a = self.lchild.isnullable()
        b = self.rchild.isnullable()
        self.nullable = a or b
        return self.nullable

    def findfirstpos(self):
        """
        Finds the set of positions in the parse tree where the first occurrence of the OrNode can be found.
        """
        self.firstpos = list(set(self.lchild.findfirstpos() + self.rchild.findfirstpos()))
        return self.firstpos

    def findlastpos(self):
        """
        Finds the set of positions in the parse tree where the last occurrence of the OrNode can be found.
        """
        self.lastpos = list(set(self.lchild.findlastpos() + self.rchild.findlastpos()))
        return self.lastpos


class LeafNode(Node):
    """
    Node class for leaf nodes (individual characters) in the regular expression parse tree.
    """

    num_of_instances = 0

    def __init__(self, parent, string):
        """
        Initializes a LeafNode object with a parent node and a string representing the character.
        """
        super().__init__(parent)
        self.string = string

        LeafNode.num_of_instances += 1
        self.number = LeafNode.num_of_instances

    def __str__(self):
        """
        Returns a string representation of the LeafNode.
        """
        return '[' + self.string + ']'

    def isnullable(self):
        """
        Checks if the LeafNode is nullable (can match an empty string).
        """
        if self.string == 'e':  # lambda node
            self.nullable = True
            return True
        else:
            self.nullable = False
            return False

    def findfirstpos(self):
        """
        Finds the set of positions in the parse tree where the first occurrence of the LeafNode can be found.
        """
        if self.string == 'e':  # lambda node
            self.firstpos = []
            return self.firstpos
        else:
            self.firstpos = [self.number, ]
            return self.firstpos

    def findlastpos(self):
        """
        Finds the set of positions in the parse tree where the last occurrence of the LeafNode can be found.
        """
        if self.string == 'e':  # lambda node
            self.lastpos = []
            return self.lastpos
        else:
            self.lastpos = [self.number, ]
            return self.lastpos
