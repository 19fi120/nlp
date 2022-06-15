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
ANE = []
for i,file in enumerate(datlist):
    if ('A5-seikai.dat' in file):
        As.append(file)
    elif ('A5-matigai.dat' in file):
        Am.append(file)
    elif ('A5-NoEntry.dat' in file):
        ANE.append(file)

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
BNE = []
for i,file in enumerate(datlist):
    if ('B5-seikai.dat' in file):
        Bs.append(file)
    elif ('B5-matigai.dat' in file):
        Bm.append(file)
    elif ('B5-NoEntry.dat' in file):
        BNE.append(file)
"""仕分け終わり"""

As_num = 0 #Aの正解の数
Am_num = 0 #Aの不正解の数
ANE_num = 0 #Aの未予測の数
countExA = 0    #Aで評価の対象外の文節の数
A_all = 0 #Aの総数

Bs_num = 0 #Bの正解の数
Bm_num = 0 #Bの不正解の数
BNE_num = 0 #Bの未予測の数
countExB = 0    #Bで評価の対象外の文節の数
B_all = 0 #Bの総数

AsAndBs = 0 #A、Bが正解の数
AsAndBm = 0 #Aが正解、Bが不正解の数
AmAndBs = 0 #Aが不正解、Bが正解の数
AmAndBm = 0 #A、Bが不正解の数

AsAndBNE = 0    #Aが正解、Bが未予測の数
AmAndBNE = 0    #Aが不正解、Bが未予測の数
BsAndANE = 0    #Bが正解、Aが未予測の数
BmAndANE = 0    #Bが不正解、Aが未予測の数
ANEAndBNE = 0   #A、Bが未予測の数

As_e = 0    #Aだけ入力かつ正解
Am_e = 0    #Aだけ入力かつ不正解
ANE_e = 0   #Aだけ入力かつ未予測
Bs_e = 0    #Bだけ入力かつ正解
Bm_e = 0    #Bだけ入力かつ不正解
BNE_e = 0   #Bだけ入力かつ未予測

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
    
    """Aが不正解している文節の集合のリスト"""
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
            if datalist[0].count("e") == 0: 
                tmp.add(datalist[0])
                A_all += 1
            else:
                countExA += 1
        Am_list.append(tmp)
        Am_num += len(tmp)
        tmp = set()
    
    """Aが未予測の文節の集合のリスト"""
    ANE_list = []
    with open(ANE[a],"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    ANE_list.append(tmp)
                    ANE_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            if datalist[0].count("e") == 0: 
                tmp.add(datalist[0])
                A_all += 1
            else:
                countExA += 1
        ANE_list.append(tmp)
        ANE_num += len(tmp)
        tmp = set()
    
    """Bが正解している文節の集合のリスト"""
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
    
    """Bが不正解している文節の集合のリスト"""
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
            if datalist[0].count("e") == 0:
                tmp.add(datalist[0])
                B_all += 1
            else:
                countExB += 1
        Bm_list.append(tmp)
        Bm_num += len(tmp)
        tmp = set()
    
    """Bが未予測の文節の集合のリスト"""
    BNE_list = []
    with open(BNE[a],"r",encoding="cp932") as fileobj:
        tmp = set()
        for b,line in enumerate(fileobj):
            if line.find("*") == 0:
                if b != 0:
                    BNE_list.append(tmp)
                    BNE_num += len(tmp)
                    tmp = set()
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            if datalist[0].count("e") == 0:
                tmp.add(datalist[0])
                B_all += 1
            else:
                countExB += 1
        BNE_list.append(tmp)
        BNE_num += len(tmp)
        tmp = set()
        
    """文節が表示されるごと"""
    for c,As_set in enumerate(As_list):
        Am_set = Am_list[c]
        Bs_set = Bs_list[c]
        Bm_set = Bm_list[c]
        ANE_set = ANE_list[c]
        BNE_set = BNE_list[c]
        
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
        
        """Aが正解、Bが未予測"""
        AsNE = As_set & BNE_set
        AsAndBNE += len(AsNE)
        
        """Aが不正解、Bが未予測"""
        AmNE = Am_set & BNE_set
        AmAndBNE += len(AmNE)
        
        """Bが正解、Aが未予測"""
        BsNE = Bs_set & ANE_set
        BsAndANE += len(BsNE)
        
        """Bが不正解、Aが未予測"""
        BmNE = Bm_set & ANE_set
        BmAndANE += len(BmNE)
        
        """A、Bが未予測"""
        ABNE = ANE_set & BNE_set
        ANEAndBNE += len(ABNE)
        
        """片方が対象外"""
        As_e += len(As_set - (Bs_set|Bm_set|BNE_set))
        Am_e += len(Am_set - (Bs_set|Bm_set|BNE_set))
        ANE_e += len(ANE_set - (Bs_set|Bm_set|BNE_set))
        
        Bs_e += len(Bs_set - (As_set|Am_set|ANE_set))
        Bm_e += len(Bm_set - (As_set|Am_set|ANE_set))
        BNE_e += len(BNE_set - (As_set|Am_set|ANE_set))
        
print(len(As))
print(len(Am))
print(len(Bs))
print(len(Bm))
print()    
print(f"Aの正解数 : {As_num}")
print(f"Aの不正解数 : {Am_num}")
print(f"Aの文字未予測数 : {ANE_num}")
print(f"Aで評価の対象外の文節の数 : {countExA}")
print(f"Aの未入力文節数 : {A_all}")
print(f"Bの正解数 : {Bs_num}")
print(f"Bの不正解数 : {Bm_num}")
print(f"Bの未予測数 : {BNE_num}")
print(f"Bで評価の対象外の文節の数 : {countExB}")
print(f"Bの未入力文節数 : {B_all}")
print()
print(f"両方正解 : {AsAndBs}")
print(f"A正解B不正解 : {AsAndBm}")
print(f"B正解A不正解 : {AmAndBs}")
print(f"両方不正解 : {AmAndBm}")
print(f"Aだけ予測正解 : {AsAndBNE}")
print(f"Aだけ予測不正解 : {AmAndBNE}")
print(f"Bだけ予測正解 : {BsAndANE}")
print(f"Bだけ予測不正解 : {BmAndANE}")
print(f"両方未予測 : {ANEAndBNE}")
print(f"Aだけ入力正解 : {As_e}")
print(f"Aだけ入力不正解 : {Am_e}")
print(f"Aだけ入力未予測 : {ANE_e}")
print(f"Bだけ入力正解 : {Bs_e}")
print(f"Bだけ入力不正解 : {Bm_e}")
print(f"Bだけ入力未予測 : {BNE_e}")