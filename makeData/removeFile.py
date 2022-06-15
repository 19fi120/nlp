# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 17:17:14 2019

@author: akira
"""

import os
import glob

path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjB"
dirs1 = []  #年月日
dirs1 = glob.glob(os.path.join(path, '*'))
#print(dirs)
dirs2 = []  #記事番号
for i,path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
    
dirs3 = []  #記事の文番号
for i,path3 in enumerate(dirs2):
    dirs3 += glob.glob(os.path.join(path3, '*'))
    
datlist = []
for i,path4 in enumerate(dirs3):
    datlist += glob.glob(os.path.join(path4,'*.dat'))
    
removelist = []
for i,file in enumerate(datlist):
    if ('A.dat' in file):   #こんな感じで削除するファイルを指定する
        removelist.append(file)
    elif ('juman2.dat' in file):
        removelist.append(file)
"""仕分け終わり"""

print(removelist)

"""ファイル削除"""
for a,file in enumerate(removelist):
    os.remove(file)