# -*- coding: utf-8 -*-
from collections import namedtuple

click_file_data = namedtuple('click_file_data', ['open_path', 'file_name', 'path_list'])

compare_dir_paths_data = namedtuple('compare_dir_paths_data',['path_dir1','path_dir2'])

add_to_edit_tree_data = namedtuple('add_to_edit_tree_data',['open_path','tree_node'])