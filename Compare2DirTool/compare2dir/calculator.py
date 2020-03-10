# -*- coding: utf-8 -*-
import os
from data.constData import *

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def walkPathDir(path_dir):
    walkLayerIndex = 1
    contain_dirs = []
    contain_files = []
    #print("当前目录:",path_dir_root)
    for root,subdirs,files in os.walk(path_dir):
        #print("第",walkLayerIndex,"层")
        walkLayerIndex += 1
        for filepath in files:
            fileAllPath = os.path.join(root, filepath)
            #print(fileAllPath)
            contain_files.append(fileAllPath)
        for subdir in subdirs:
            dirAllPath = os.path.join(root,subdir)
            #print(dirAllPath)
            contain_dirs.append(dirAllPath)
    return contain_dirs,contain_files

def getRelativePath(root,path_dir1):
    return root.replace(path_dir1,"")

def diffTwoFiles(file1,file2):
    if file1 == file2:
        return 0
    file1.replace("/","\\")
    file2.replace("/","\\")
    exeStr = "fc " + file1 + " " + file2
    try:
        execCmd(exeStr)
        exeStr = "echo %errorlevel%"
        result =  int(execCmd(exeStr)[0])
        return result  # -1表达式错误，0相同，1不同，2文件不存在
    except:
        print("exeStr error, str is:",exeStr)
        return -1

def isExistInOtherDir(path,src,test):
    replacePath = path.replace(src,test)
    if os.path.exists(replacePath):
        if os.path.isdir(path) == os.path.isdir(replacePath):
            return True
    return False

def compare_different_files_of_dirs(pathfiles,path_dir1,path_dir2,only_dir_files,modified_files):
    frame_compare_cnt = 0
    compare_cnt = 0
    for pathfile in pathfiles:
        relativePath = getRelativePath(pathfile,path_dir1)
        if relativePath in only_dir_files or relativePath in modified_files:
            continue
        if isExistInOtherDir(pathfile,path_dir1,path_dir2):
            #两个目录都存在文件
            dir2file = pathfile.replace(path_dir1, path_dir2)
            if diffTwoFiles(pathfile,dir2file) == 0:
                #完全相同
                pass
            else:
                #两文件不同，加入修改目录
                modified_files.add(relativePath)
        else:
            #目录1独有
            only_dir_files.add(relativePath)
        frame_compare_cnt += 1
        compare_cnt += 1
        if frame_compare_cnt >= 3:
            print("this frame has done：",(compare_cnt/len(pathfiles)))
            from mymvc.GameFacade import GameFacade
            from compareCommand import CompareCommand
            GameFacade().sendNotification(CompareCommand.show_compare_progress_cmd,round(100*compare_cnt/len(pathfiles),2) )
            yield
            frame_compare_cnt = 0

def compare_different_dirs_of_dirs(pathdirs,path_dir1,path_dir2,only_dir_dirs):
    for pathdir in pathdirs:
        relativePath = getRelativePath(pathdir, path_dir1)
        if relativePath in only_dir_dirs:
            continue
        if isExistInOtherDir(pathdir, path_dir1, path_dir2):
            pass
        else:
            only_dir_dirs.add(relativePath)

def addFilePathToTree(file,tree):
    file = file.replace('\\','/')
    tree.addFilePathToTree(file)

def createFileTree(treename,rootname,only_files,only_dirs):
    from common.tree import Tree, TreeNode
    tree = Tree(TreeNode(rootname),treename)
    for only_file in only_files:
        addFilePathToTree(only_file,tree)
    for dir in only_dirs:
        addFilePathToTree(dir, tree)
    return tree

def compare2DirDifferents(path_dir1,path_dir2):
    #返回值
    different_dirs_cnt = 0
    different_files_cnt = 0

    only_dir1_dirs = set()
    only_dir2_dirs = set()
    only_dir1_files = set()
    only_dir2_files = set()
    modified_files = set()

    print("开始比较目录差异")
    path1dirs, path1files = walkPathDir(path_dir1)
    print("目录1包含:",len(path1dirs),"个子目录，",len(path1files),"个文件")
    path2dirs, path2files = walkPathDir(path_dir2)
    print("目录2包含:", len(path2dirs), "个子目录，", len(path2files), "个文件")

    #耗时比较操作,用协程分片回调进度
    yield compare_different_files_of_dirs(path1files, path_dir1, path_dir2, only_dir1_files, modified_files)
    yield compare_different_files_of_dirs(path2files, path_dir2, path_dir1, only_dir2_files, modified_files)

    compare_different_dirs_of_dirs(path1dirs,path_dir1,path_dir2,only_dir1_dirs)
    compare_different_dirs_of_dirs(path2dirs,path_dir2,path_dir1,only_dir2_dirs)

    # 遍历目录的文件，得到相异的文件，加上相异目录，构建树
    only_dir1_dirs = list(only_dir1_dirs)
    only_dir2_dirs = list(only_dir2_dirs)
    only_dir1_files = list(only_dir1_files)
    only_dir2_files = list(only_dir2_files)
    modified_files = list(modified_files)
    different_dirs_cnt = len(only_dir1_dirs) + len(only_dir2_dirs)
    different_files_cnt = len(only_dir1_files) + len(only_dir2_files) + len(modified_files)

    only_dir1_tree = createFileTree(dir1_tree_name,path_dir1,only_dir1_files,only_dir1_dirs)
    only_dir2_tree = createFileTree(dir2_tree_name,path_dir2,only_dir2_files,only_dir2_dirs)
    modified_tree = createFileTree(modified_tree_name,"modify_root",modified_files,[])

    compareResult = {
        "different_dirs_cnt":different_dirs_cnt,
        "different_files_cnt":different_files_cnt,
        "only_dir1_tree":only_dir1_tree,
        "only_dir2_tree":only_dir2_tree,
        "modified_tree":modified_tree,
        "path_dir1":path_dir1,
        "path_dir2":path_dir2,
    }

    from compareCommand import CompareCommand
    from mymvc.GameFacade import GameFacade
    GameFacade().sendNotification(CompareCommand.hide_compare_progress_cmd)
    GameFacade().sendNotification(CompareCommand.show_compare_result_cmd, compareResult)

