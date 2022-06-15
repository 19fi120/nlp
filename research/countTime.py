import os
import glob
import matplotlib.pyplot as plt

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
    
filelist = []
for i,file in enumerate(datlist):
    if('result.dat' in file):
        filelist.append(file)

timelist = []   #1文の作業時間のリスト
timeover = []   #作業時間が長すぎる文のリスト
bunsetu = 0 #文節数
sumtime = 0 #総作業時間(作業時間が長すぎる文は除く)
for i,file in enumerate(filelist):
    tmp = []
    bun = 0
    with open(filelist[i],"r",encoding="utf_8") as fileobj:
        start = 0
        end = 0
        time = 0
        for a,line in enumerate(fileobj):
            if line.count("#") > 0:
                aline = line.rstrip()
                datalist = aline.split(" ")
                if a == 0:
                    start = int(datalist[-1])
                else:
                    end = int(datalist[-1])
            
            if line.count("*") > 0:
                bunsetu += 1
                bun += 1
                    
        time = end - start
        if time < 900:
            timelist.append(time)
            sumtime += time
        else:
            print(fileobj)
            timeover.append([bun,time])

print(bunsetu)
timelist.sort()
print(timelist[-20:])
print(f"アノテーション総時間 : {sumtime}秒({int(int(sumtime/60)/60)}時間 {int(sumtime/60)%60}分 {sumtime%60}秒)")
print(f"平均 : {sumtime/len(timelist)}秒")
print(timeover)
"""
ヒストグラム作成用
new_fileobj = open("C:/Users/akira/Desktop/data.txt","w",encoding = "utf_8")

hist = 0
bins = 1
for i,t in enumerate(timelist):
    new_fileobj.write(str(t)+"\n")
    if t > 30*bins:
        print(f"{30*(bins-1)} ~ {30*bins} : {hist}")
        hist = 0
        bins += 1
    hist += 1
print(f"{30*(bins-1)} ~ {30*bins} : {hist}")

new_fileobj.close()
plt.hist(timelist,bins=30,range=(0,900))#15分=900秒
"""





