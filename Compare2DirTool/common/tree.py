# -*- coding: utf-8 -*-

class Tree:

    def __init__(self,treenode,name = ""):
        self.name = name
        if treenode and isinstance(treenode, TreeNode):
            self.root = treenode
        else:
            raise ValueError('root should be TreeNode obj')

    def add_child_to_parent(self,parentpath,newnode):
        #child 是treenode，可以是子树
        parentNode = self.find_child_by_path(parentpath)
        if parentNode:
            parentNode.add_child(newnode)
        else:
            print("[Tree error] parent not found!",parentpath)

    def find_child_by_name(self,name):
        return self.root.find_child_by_name(name)

    def find_child_by_path(self,path):
        return self.root.find_child_by_path(path)

    def delete_child_by_path(self,path):
        return self.root.del_child_by_path(path)

    def dfs_get_treenodes(self):
        return self.root.dfs_get_child_nodes()

    def addFilePathToTree(self,file):
        from common.tree import TreeNode
        filestrarr = file.split("/")
        filestrarr = [file for file in filestrarr if file.strip() != ""]
        pathNode = self.root
        for pathfile in filestrarr:
            if pathNode:
                childNode = pathNode.get_child(pathfile)
                if childNode is None:
                    newNode = TreeNode(pathfile)
                    pathNode.add_child(newNode)
                    pathNode = newNode
                else:
                    pathNode = childNode


class TreeNode:

    def __init__(self,name,parent = None):
        super(TreeNode,self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}
        self.data = {}

    @property
    def path(self):
        if self.parent:
            return '%s/%s' % (self.parent.path.strip(), self.name)
        else:
            return self.name

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
    def del_child_all_by_name(self, name):
        if name in self.child:
            del self.child[name]
        else:
            for key,child in self.child.items():
                child.del_child_all_by_name(name)

    def del_child_one_by_name(self,name):
        if name in self.child:
            del self.child[name]

    def del_child_by_path(self,path):
        child = self.find_child_by_path(path)
        if child and child.parent:
            parent = child.parent
            parent.del_child_one_by_name(child.name)

    def find_child_by_name(self,name):
        node = self.get_child(name)
        if node:
            return node
        else:
            for key,child in self.child.items():
                if child and child.get_child(name):
                    return child.get_child(name)
        return None

    def find_child_by_path(self,path):
        #以/隔开的字符串
        for key, child in self.child.items():
            if path == child.path:
                return child
            if path.find(child.path) > -1:
                result = child.find_child_by_path(path)
                if result:
                    return result
        return None

    def dfs_get_child_nodes(self):
        childs = []
        for key, child in self.child.items():
            if child:
                childs.append(child)
                childs.extend(child.dfs_get_child_nodes())
        return childs