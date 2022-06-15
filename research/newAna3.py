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
    
As = []
Am = []
for i,file in enumerate(datlist):
    if ('A3-seikai.dat' in file):
        As.append(file)
    elif ('A3-matigai.dat' in file):
        Am.append(file)

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
    
Bs = []
Bm = []
for i,file in enumerate(datlist):
    if ('B3-seikai.dat' in file):
        Bs.append(file)
    elif ('B3-matigai.dat' in file):
        Bm.append(file)

As_num = 0 #Aの正解の数
Am_num = 0 #Aの不正解の数
A_all = 0 #Aの総数

Bs_num = 0 #Bの正解の数
Bm_num = 0 #Bの不正解の数
B_all = 0 #Bの総数

AsAndBs = 0 #A、Bが正解の数
AsAndBm = 0 #Aが正解、Bが不正解の数
AmAndBs = 0 #Aが不正解、Bが正解の数
AmAndBm = 0 #A、Bが不正解の数

for a,file in enumerate(As):
    """Aが正解している文節の集合のリスト"""
    As_list = []
    with open(file,"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    As_list.append(tmp)
                    As_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            tmp.add(datalist[0])
            A_all += 1
        As_list.append(tmp)
        As_num += len(tmp)
        tmp = set()
    
    """Aが不正解している文節の集合"""
    Am_list = []
    with open(Am[a],"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    Am_list.append(tmp)
                    Am_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            tmp.add(datalist[0])
            A_all += 1
        Am_list.append(tmp)
        Am_num += len(tmp)
        tmp = set()
    
    """Bが正解している文節の集合"""
    Bs_list = []
    with open(Bs[a],"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    Bs_list.append(tmp)
                    Bs_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            tmp.add(datalist[0])
            B_all += 1
        Bs_list.append(tmp)
        Bs_num += len(tmp)
        tmp = set()
    
    """Aが不正解している文節の集合"""
    Bm_list = []
    with open(Bm[a],"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    Bm_list.append(tmp)
                    Bm_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            tmp.add(datalist[0])
            B_all += 1
        Bm_list.append(tmp)
        Bm_num += len(tmp)
        tmp = set()
    
    """文節が表示されるごと"""
    for c,As_set in enumerate(As_list):
        Am_set = Am_list[c]
        Bs_set = Bs_list[c]
        Bm_set = Bm_list[c]
        
        """A、Bが正解"""
        ss = As_set & Bs_set
        AsAndBs += len(ss)
    
        """Aが正解、Bが不正解"""
        sm = As_set & Bm_set
        AsAndBm += len(sm)
        
        """Aが不正解、Bが正解"""
        ms = Am_set & Bs_set
        AmAndBs += len(ms)
    
        """A、Bが不正解"""
        mm = Am_set & Bm_set
        AmAndBm += len(mm)
        
print(len(As))
print(len(Am))
print(len(Bs))
print(len(Bm))
print()    
print(f"Aの正解数 : {As_num}")
print(f"Aの不正解数 : {Am_num}")
print(f"Aの未入力文節数 : {A_all}")
print(f"Bの正解数 : {Bs_num}")
print(f"Bの不正解数 : {Bm_num}")
print(f"Bの未入力文節数 : {B_all}")
print()
print(f"両方正解 : {AsAndBs}")
print(f"A正解B不正解 : {AsAndBm}")
print(f"B正解A不正解 : {AmAndBs}")
print(f"両方不正解 : {AmAndBm}")