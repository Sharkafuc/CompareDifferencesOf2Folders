# -*- coding: utf-8 -*-
import os

def isImageFile(file_name):
    ext = os.path.splitext(file_name)[1]
    ext = ext.lower()
    if ext == '.jpg' or ext == '.png' or ext == '.jpeg' or ext == '.bmp':
        return True
    else:
        return False

