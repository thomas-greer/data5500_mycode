"""
Promp:
Help me understand deleting a node from a binary search tree 


Deleting a node from a search tree is more complicated than
searching or inserting in a tree. I would say there are 3 main 
cases: Childless, single child, or double child. Childless
would be the easiest just by removing this node wouldnt change
the aspect of the tree. A single child would be the second
easiest, with just removing the node, and moving the child
of the node to the parent of the node removed. A double child
would be the hardest since you have to replace the organizaion.
The solution i would use is to fine the left most node on the right
child of the node to then replace the removed node. That way
you only remove the orignal node, and the childless one at
the bottom. That would be the simplest solution in my opinion.

The challenges of deleting a node is to make sure the binary tree's
form isnt lost when removing. Like leaving a node without a parent
or messing up the organization of the tree. Duplication of the nodes
would also be a problem if removing them is done wrong.
"""