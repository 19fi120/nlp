import os
import glob

"""ファイル仕分け"""
path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjA"
dirs1 = []  #年月日
dirs1 = glob.glob(os.path.join(path, '*'))
dirs2 = []  #記事番号
for i,path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
dirs3 = []  #記事の文番号
for i,path3 in enumerate(dirs2):
    dirs3 += glob.glob(os.path.join(path3, '*'))
datlist = []
for i,path4 in enumerate(dirs3):
    datlist += glob.glob(os.path.join(path4,'*.dat'))
    
A1s = []
A1m = []
for i,file in enumerate(datlist):
    if ('A1-seikai.dat' in file):
        A1s.append(file)
    elif ('A1-matigai.dat' in file):
        A1m.append(file)

path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjB"
dirs1 = []  #年月日
dirs1 = glob.glob(os.path.join(path, '*'))
dirs2 = []  #記事番号
for i,path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
dirs3 = []  #記事の文番号
for i,path3 in enumerate(dirs2):
    dirs3 += glob.glob(os.path.join(path3, '*'))
datlist = []
for i,path4 in enumerate(dirs3):
    datlist += glob.glob(os.path.join(path4,'*.dat'))
    
B1s = []
B1m = []
for i,file in enumerate(datlist):
    if ('B1-seikai.dat' in file):
        B1s.append(file)
    elif ('B1-matigai.dat' in file):
        B1m.append(file)

A1s_num = 0 #Aの正解の数
A1m_num = 0 #Aの不正解の数
B1s_num = 0 #Bの正解の数
B1m_num = 0 #Bの不正解の数

AsAndBs = 0 #A、Bが正解の数
AsAndBm = 0 #Aが正解、Bが不正解の数
AmAndBs = 0 #Aが不正解、Bが正解の数
AmAndBm = 0 #A、Bが不正解の数

for a,file in enumerate(A1s):
    """Aが正解している文節の集合"""
    A1s_set = set() #("文節ID",...)
    with open(file,"r",encoding="cp932") as fileobj:
        for b,line in enumerate(fileobj):
            aline = line.rstrip()
            datalist = aline.split(" ")
            A1s_set.add(datalist[0])
    A1s_set = frozenset(A1s_set)
    A1s_num += len(A1s_set)
    
    """Aが不正解している文節の集合"""
    A1m_set = set() #("文節ID",...)
    with open(A1m[a],"r",encoding="cp932") as fileobj:
        for b,line in enumerate(fileobj):
            aline = line.rstrip()
            datalist = aline.split(" ")
            A1m_set.add(datalist[0])
    A1m_set = frozenset(A1m_set)
    A1m_num += len(A1m_set)
    
    """Bが正解している文節の集合"""
    B1s_set = set() #("文節ID",...)
    with open(B1s[a],"r",encoding="cp932") as fileobj:
        for b,line in enumerate(fileobj):
            aline = line.rstrip()
            datalist = aline.split(" ")
            B1s_set.add(datalist[0])
    B1s_set = frozenset(B1s_set)
    B1s_num += len(B1s_set)
    
    """Bが不正解している文節の集合"""
    B1m_set = set() #("文節ID",...)
    with open(B1m[a],"r",encoding="cp932") as fileobj:
        for b,line in enumerate(fileobj):
            aline = line.rstrip()
            datalist = aline.split(" ")
            B1m_set.add(datalist[0])
    B1m_set = frozenset(B1m_set)
    B1m_num += len(B1m_set)

    """A、Bが正解"""
    ss = A1s_set & B1s_set
    AsAndBs += len(ss)
    
    """Aが正解、Bが不正解"""
    sm = A1s_set & B1m_set
    AsAndBm += len(sm)
    
    """Aが不正解、Bが正解"""
    ms = A1m_set & B1s_set
    AmAndBs += len(ms)
    
    """A、Bが不正解"""
    mm = A1m_set & B1m_set
    AmAndBm += len(mm)
    
print(f"Aの正解数 : {A1s_num}")
print(f"Aの不正解数 : {A1m_num}")
print(f"Bの正解数 : {B1s_num}")
print(f"Bの不正解数 : {B1m_num}")
print()
print(f"両方正解 : {AsAndBs}")
print(f"Aだけ正解 : {AsAndBm}")
print(f"Bだけ正解 : {AmAndBs}")
print(f"両方不正解 : {AmAndBm}")