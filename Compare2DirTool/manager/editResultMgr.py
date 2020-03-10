# -*- coding: utf-8 -*-
from common.Singleton import Singleton
from common.tree import *
from data.constData import *
import json
import os

class EditResultMgr(metaclass=Singleton):

    def __init__(self):
        super(EditResultMgr, self).__init__()

    def writeEditTreeToResult(self,treedata,resultfile):
        all_edit_files = []
        root_name = ""
        #读出原本的内容    
        if os.path.exists(resultfile):
            with open(resultfile,'r',encoding='utf-8') as f:
                readLines = f.readlines()
                file_list = readLines[1:]
                #略过本次编辑的目录
                cur_edit_root = treedata.root.name
                for file in file_list:
                    if file.find(cur_edit_root) > -1:
                        pass
                    else:
                        filename = file.replace("\n","")
                        all_edit_files.append(filename)

        if treedata and isinstance(treedata,Tree):

            all_tree_nodes = (treedata.dfs_get_treenodes())
            all_nodes_paths = [tree.path for tree in all_tree_nodes]

            all_edit_files.extend(all_nodes_paths)
            if len(all_edit_files) > 0:
                root_name = self.getEditRoot(all_edit_files)
                with open(resultfile,'w',encoding='utf-8') as f:
                    f.write(edit_result_file_root+root_name + "\n")
                    for treenode in all_tree_nodes:
                        f.write(treenode.path + "\n")

    def getEditRoot(self,all_edit_files):
        i = 0
        first_file = all_edit_files[0]
        first_file_paths = first_file.split('/')
        checklen = len(first_file_paths)
        while i < checklen:
            ch = first_file_paths[i]
            for file in all_edit_files:
                file_paths = file.split('/')
                if len(file_paths) > i:
                    node_char = file_paths[i]
                    if ch != node_char:
                        patharray = first_file_paths[0:i]
                        return '/'.join(patharray)
                else:
                    patharray = first_file_paths[0:i]
                    return '/'.join(patharray)
            i += 1
        patharray = first_file_paths[0:i]
        return '/'.join(patharray)

    def getTargetDirResult(self,resultfile,targetdir):
        targetDirResults = []
        if os.path.exists(resultfile):
            with open(resultfile, 'r', encoding='utf-8') as f:
                readLines = f.readlines()
                file_list = readLines[1:]
                cur_edit_root = targetdir
                for file in file_list:
                    if file.find(cur_edit_root) > -1:
                        filename = file.replace('\n', "")
                        targetDirResults.append(filename)
        return targetDirResults