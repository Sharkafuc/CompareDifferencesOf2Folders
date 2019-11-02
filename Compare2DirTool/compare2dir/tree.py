# -*- coding: utf-8 -*-

class Tree:

    def __init__(self,treenode,name = ""):
        self.name = name
        if treenode and isinstance(treenode, TreeNode):
            self.root = treenode
        else:
            raise ValueError('root should be TreeNode obj')

    def add_child_to_parent(self,parentname,newnode):
        parentNode = self.root.find_child_by_name(parentname)
        if parentNode:
            parentNode.add_child(newnode)
        else:
            print("parent name not found")

    def find_child_by_name(self,name):
        return self.root.find_child_by_name(name)

class TreeNode:

    def __init__(self,name,parent = None):
        super(TreeNode,self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}
        self.data = {}

    #get当前节点的child
    def get_child(self,name):
        return self.child.get(name)

    # get当前节点的childs
    def get_childs(self):
        return self.child

    #当前节点增加child
    def add_child(self, obj):
        if obj == None or not isinstance(obj, TreeNode):
            raise ValueError('TreeNode only add another TreeNode obj as child')

        if obj:
            obj.parent = self
            self.child[obj.name] = obj
        return obj

    #当前节点删除child
    def del_child(self, name):
        if name in self.child:
            del self.child[name]
        else:
            for key,child in self.child.items():
                child.del_child(name)

    def find_child_by_name(self,name):
        node = self.get_child(name)
        if node:
            return node
        else:
            for key,child in self.child.items():
                if child and child.get_child(name):
                    return child.get_child(name)
        return None

    @property
    def path(self):
        if self.parent:
            return '%s/%s' % (self.parent.path.strip(), self.name)
        else:
            return self.name
