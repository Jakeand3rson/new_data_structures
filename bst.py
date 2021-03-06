# http://blog.shayanjaved.com/2012/01/14/binary-search-tree-in-python/
# http://interactivepython.org/XSKWZ/LpOMZ/courselib/static/pythonds/Trees/bst.html
import timeit
import random
'''commented it out because its a dick if you run this without pointing it to a file to print in.'''
# import subprocess
from collections import deque


class BSTNode(object):
    '''Instantiate Node and add helper functions'''
    def __init__(self, val, parent=None, left_child=None, right_child=None):
        self.val = val
        self.parent = parent
        self.left = left_child
        self.right = right_child
        self.height = 0
        self.balance = 0

    def is_root(self):
        '''Helper function for root node'''
        return not self.parent

    def is_leaf(self):
        ''''Helper function for acknowledging leaf'''
        return not (self.right_child or self.left_child)

    def is_left(self):
        '''Helper fuction for finding left child. Might be redundent with is_left
           Will decide later........'''
        if self.parent is None:
            return self.parent
        else:
            return self is self.parent.left_child

    def update_height(self, bubble_up=True):
        '''If bubble_up is True, we go up the tree correcting height/balance
           if not we will just correct the node'''
        if self.left_child is None:
            # set the left tree to zero
            left_height = 0
        else:
            left_height = self.left_child.height + 1
        if self.right_child is None:
            # set the right tree to zero
            right_height = 0
        else:
            right_height = self.right_child.height + 1
            # we want to be able to balance even if we don't change the height

        self.balance = left_height - right_height
        height = max(left_height, right_height)
        if self.height != height:
            self.height = height
            if self.parent is not None:
                # We only bubble up if the height changes
                if bubble_up:
                    self.parent.update_height()

    def _get_dot(self):
        """recursively prepare a dot graph entry for this node."""
        if self.left is not None:
            yield "\t%s -> %s;" % (self.val, self.left.val)
            for i in self.left._get_dot():
                yield i
        elif self.right is not None:
            r = random.randint(0, 1e9)
            yield "\tnull%s [shape=point];" % r
            yield "\t%s -> null%s;" % (self.val, r)
        if self.right is not None:
            yield "\t%s -> %s;" % (self.val, self.right.val)
            for i in self.right._get_dot():
                yield i
        elif self.left is not None:
            r = random.randint(0, 1e9)
            yield "\tnull%s [shape=point];" % r
            yield "\t%s -> null%s;" % (self.val, r)


class BST(object):
    '''Instantiate binary search tree'''
    def __init__(self, vals=None):
        self.root = None
        self._size = 0

    def size(self):
        '''Will return integer size of BST'''
        return self._size

    def insert(self, val):
        '''Inserts the data in val into BST'''
        if self.root is None:
            self.root = BSTNode(val)
            self._size += 1
            return
        current_node = self.root
        while True:
            if current_node.val > val:
                if current_node.left:
                    current_node = current_node.left
                else:
                    current_node.left = BSTNode(val)
                    self._size += 1
                    break
            elif current_node.val < val:
                if current_node.right:
                    current_node = current_node.right
                else:
                    current_node.right = BSTNode(val)
                    self._size += 1
                    break
            else:
                break

    def contains(self, val):
        '''Returns true if data in val is in BST'''
        if self.root is None:
            return False
        current_node = self.root
        while True:
            if current_node.val > val:
                if current_node.left:
                    current_node = current_node.left
                else:
                    return False
            elif current_node.val < val:
                if current_node.right:
                    current_node = current_node.right
                else:
                    return False
            else:
                return True

    def depth(self):
        '''Returns total number of levels in BST as interger'''
        if self.root is None:
            return 0
        return self._depth(1, self.root)

    def _depth(self, curr_depth, local_root):
        '''Helper function for depth'''
        l_depth = r_depth = 0
        if local_root.left:
            l_depth = self._depth(curr_depth + 1, local_root.left)
        if local_root.right:
            r_depth = self._depth(curr_depth + 1, local_root.right)
        return max(curr_depth, l_depth, r_depth)

    def is_balanced(self):
        '''Return positive or negative integer to represent tree balance'''
        ret_val = 0
        if self.root is None:
            return ret_val
        if self.root.left:
            ret_val += self._depth(1, self.root.left)
        if self.root.right:
            ret_val -= self._depth(1, self.root.right)
        return ret_val

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def get_dot(self):
        """return the tree with root 'self' as a dot graph for visualization"""
        return "digraph G{\n%s}" % ("" if self.root.val is None else (
            "\t%s;\n%s\n" % (
                self.root.val,
                "\n".join(self.root._get_dot())
            )
        ))

    def in_order(self):
        return self._in_order(self.root)

    def _in_order(self, leaf):
        if leaf is None:
            return
        for val in self._in_order(leaf.left):
            yield val
        yield leaf.val
        for val in self._in_order(leaf.right):
            yield val

    def pre_order(self):
        return self._pre_order(self.root)

    def _pre_order(self, leaf):
        if leaf is None:
            return
        yield leaf.val
        for val in self._pre_order(leaf.left):
            yield val
        for val in self._pre_order(leaf.right):
            yield val

    def post_order(self):
        return self._post_order(self.root)

    def _post_order(self, leaf):
        if leaf is None:
            return
        for val in self._post_order(leaf.left):
            yield val
        for val in self._post_order(leaf.right):
            yield val
        yield leaf.val

    def breadth_traversal(self):
        x = deque()
        x.append(self.root)
        while x:
            leaf = x.popleft()
            yield leaf.val
            if leaf.left:
                x.append(leaf.left)
            if leaf.right:
                x.append(leaf.right)

    def delete(self, val):
        self.root = self._delete(val, self.root)
        return None

    def _delete(self, val, leaf):
        def _descendants(leaf):
            if leaf.left:
                return _descendants(leaf.left)
            else:
                return leaf.val

        if not leaf:
            return None

        if leaf.val == val:
            self._size -= 1
            if leaf.left and leaf.right:
                leaf.val = _descendants(leaf.right)
                leaf.right = self._delete(leaf.val, leaf.right)
                return leaf
            elif leaf.left and not leaf.right:
                return leaf.left
            elif not leaf.left and leaf.right:
                return leaf.right
            else:
                return None

        elif leaf.val < val:
            if leaf.right:
                leaf.right = self._delete(val, leaf.right)
            return leaf

        else:
            if leaf.left:
                leaf.left = self._delete(val, leaf.left)
            return leaf

    def l_rotate(self, node):
        x = node.left
        node.left = x.right
        x.right = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        x.height = max(self.height(x.left), node.height) + 1
        return x

    def r_rotate(self, node):
        x = node.right
        node.right = x.left
        x.left = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        x.height = max(self.height(x.right), node.height) + 1
        return x

    def ll_rotate(self, node):
        node.left = self.r_rotate(node.left)
        return self.l_rotate(node)

    def rr_rotate(self, node):
        node.right = self.l_rotate(node.right)
        return self.r_rotate(node)

    ''' This is the insert function for the AVL tree that will balance itself on insert'''
    def put(self, val):
        if not self.root:
            self.root = BSTNode(val)
        else:
            self.root = self._put(val, self.root)

    def _put(self, val, node):
        if node is None:
            node = BSTNode(val)
        elif val < node.val:
            node.left = self._put(val, node.left)
            if (self.height(node.left) - self.height(node.right)) == 2:
                if val < node.left.val:
                    node = self.l_rotate(node)
                else:
                    node = self.ll_rotate(node)
        elif val > node.val:
            node.right = self._put(val, node.right)
            if (self.height(node.right) - self.height(node.left)) == 2:
                if val < node.right.val:
                    node = self.rr_rotate(node)
                else:
                    node = self.r_rotate(node)

        node.height = max(self.height(node.right), self.height(node.left)) + 1
        return node

    def rotate_left(self, root):
        left = root.is_left()
        pivot = root.right_child

        if pivot is None:
            return
        root.right_child = pivot.left_child
        if pivot.left_child is not None:
            root.right_child.parent = root
        pivot.left_child = root
        pivot.parent = root.parent
        root.parent = pivot
        if left is None:
            self.root = pivot
        elif left:
            pivot.parent.left_child = pivot
        else:
            pivot.parent.right_child = pivot
        root.update_height(False)
        pivot.update_height(False)

    def rotate_right(self, root):
        left = root.is_left()
        pivot = root.left_child
        if pivot is None:
            return
        root.left_child = pivot.right_child
        if pivot.right_child is not None:
            root.left_child.parent = root
        pivot.right_child = root
        pivot.parent = root.parent
        root.parent = pivot
        if left is None:
            self.root = pivot
        elif left:
            pivot.parent.left_child = pivot
        else:
            pivot.parent.right_child = pivot
        root.update_height(False)
        pivot.update_height(False)

    def find_leftmost(self, node):
        if node.left_child is None:
            return node
        else:
            return self.find_leftmost(node.left_child)

    def find_rightmost(self, node):
        if node.right_child is None:
            return node
        else:
            return self.find_rightmost(node.right_child)

    def find_next(self, val):
        node = self.find(val)
        if (node is None) or (node.val != val):
            return None
        else:
            right_child = node.right_child
            if right_child is not None:
                node = self.find_leftmost(right_child)
            else:
                parent = node.parent
                while(parent is not None):
                    if node is parent.left_child:
                        break
                    node = parent
                    parent = node.parent
                node = parent
            if node is None:
                return node
            else:
                return node.val

    def find_prev(self, val):
        node = self.find(val)
        if (node is None) or (node.val != val):
            return None
        else:
            left_child = node.left_child
            if left_child is not None:
                node = self.find_leftmost(left_child)
            else:
                parent = node.parent
                while(parent is not None):
                    if node is parent.right_child:
                        break
                    node = parent
                    parent = node.parent
                node = parent
            if node is None:
                return node
            else:
                return node.val

    def find(self, val, node=None):
        if node is None:
            node = self.root
            if self.root is None:
                return None
            else:
                return self.find(val, self.root)
        elif node.val == val:
            return node
        elif val < node.val:
            if node.left_child is None:
                return node
            else:
                return self.find(val, node.left_child)
        else:
            if node.right_child is None:
                return node
            else:
                return self.find(val, node.right_child)

    def balance(self, node):
        ''' There are four posabilities for rotation
            left-left=LL right-right=RR
            left-right=LR right-left=RL'''
        node.update_height(False)
        if node.balance == 2:
            if node.left_child.balance != -1:
                # LL rotation
                self.rotate_right(node)
                if node.parent.parent is not None:
                    self.balance(node.parent.parent)
            else:
                # LR rotation
                self.rotate_left(node.left_child)
                self.balance(node)
        elif node.balance == -2:
            if node.right_child.balance != 1:
                # RR rotation
                self.rotate_left(node)
                if node.parent.parent is not None:
                    self.balance(node.parent.parent)

            else:
                # RL rotation
                self.rotate_right(node.right_child)
                self.balance(node)
        else:
            if node.parent is not None:
                self.balance(node.parent)

    def sort(self, tree_maker, ascending=True):
        b = BST()
        for item in tree_maker:
            b.insert(item)
        ret_val = []
        if ascending:
            node = b.find_leftmost(b.root)
            if node is not None:
                val = node.val
            else:
                val = node
            while (val is not None):
                ret_val.append(val)
                val = b.find_next(val)

        else:
            node = b.find_rightmost(b.root)
            if node is not None:
                val = node.val
            else:
                val = node
            while (val is not None):
                ret_val.append(val)
                val = b.find_prev(val)
        return ret_value


if __name__ == '__main__':

    # x = range(100)
    # bst = BST()
    # for i in x:
    #     bst.put(i)
    # dot_graph = bst.get_dot()
    # t = subprocess.Popen(["dot", "-Tpng"], stdin=subprocess.PIPE)
    # t.communicate(dot_graph)

    def easy_tree():
        x = random.sample(range(100), 100)
        bst = BST()
        bst.insert(50)
        for i in x:
            bst.insert(i)
        bst.insert(42.1)
        bst.contains(42.1)

    def hard_tree():
        x = range(100)
        bst = BST()
        for i in x:
            bst.insert(i)
        bst.insert(42.1)
        bst.contains(42.1)

    print(timeit.Timer("easy_tree()", setup="from __main__ import easy_tree").timeit(number=1000))
    print(timeit.Timer("hard_tree()", setup="from __main__ import hard_tree").timeit(number=1000))
