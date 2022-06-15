import os
import glob

"""仕分け"""
path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjA"
dirs1 = []  #年月日
dirs1 = glob.glob(os.path.join(path, '*'))
dirs2 = []  #記事番号
for i,path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
dirs3 = []  #記事の文番号
for i,path3 in enumerate(dirs2):
    dirs3 += glob.glob(os.path.join(path3, '*'))
datlist = []#datファイルのリスト
for i,path4 in enumerate(dirs3):
    datlist += glob.glob(os.path.join(path4,'*.dat'))
    
filelist = []   #作業結果のファイル
answerlist = [] #正解データのファイル
for i,file in enumerate(datlist):
    if('result.dat' in file):
        filelist.append(file)
    elif ('juman.dat' in file):
        pass
    elif ('A1-seikai.dat' in file):
        pass
    elif ('A1-matigai.dat' in file):
        pass
    elif ('A2-seikai.dat' in file):
        pass
    elif ('A2-matigai.dat' in file):
        pass
    elif ('A3-seikai.dat' in file):
        pass
    elif ('A3-matigai.dat' in file):
        pass
    elif ('A4-seikai.dat' in file):
        pass
    elif ('A4-matigai.dat' in file):
        pass
    elif ('A4-NoEntry.dat' in file):
        pass
    elif ('A5-seikai.dat' in file):
        pass
    elif ('A5-matigai.dat' in file):
        pass
    elif ('A5-NoEntry.dat' in file):
        pass
    else:
        answerlist.append(file)

"""作成するファイル名"""
new_filelist = []   #分析のために作成するファイル名のリスト
for i,path in enumerate(dirs3):
    new_filelist.append(path+"/A2-matigai.dat")

n = 0   #文数
br = 0  #文正解の数
num = 0 #文節数
r = 0   #正解の数
f = 0   #不正解の数

p = True    #文正解数を数えるための変数
idnum = 0   #文節数を数えるための変数

mi = 0  #係り先が未入力である文節の正解数

"""1文ずつ評価を行う"""
for i,file in enumerate(filelist):
    #if file.count("950104")>0:
        #continue
    
    n += 1
    p = True
    
    """正解データのリストを作る"""
    answer = [] #["0文節目の正解の係り先文節ID","1文節目の正解の係り先文節ID",...]
    with open(answerlist[i],"r",encoding="utf_8") as fileobj:
        for z,line in enumerate(fileobj) :            
            if line.find("*") == 0:
                aline = line.rstrip()
                datalist = aline.split(" ")
                s = datalist[2]
                answer.append(s[:-1])
                    
    """文節ごとの作業結果のリストを作る"""
    bunsetsulist = []   #[["文節ID","予測した係り先文節ID","得点"],...,["未入力文節ID","対応する正解の文節ID","予測した文字列","得点"],...]
    with open(file,"r",encoding="utf_8") as fileobj:
        for y,line in enumerate(fileobj) :            
            if line.count("#")>0:
                continue
            if line.count("*")>0:
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            bunsetsulist.append(datalist)

    """ファイルを作成"""
    new_fileobj = open(new_filelist[i],"w",encoding = "utf_8")
    print(new_filelist[i])
    
    """評価"""
    count = 0   #何文節目までが既入力となっているかを示す
    for x,line in enumerate(bunsetsulist) :
        if int(line[0]) < 0:    #未入力文節は使わない
            continue

        if int(line[0]) == 0:   #既入力の文節が追加される
            print("*",count)
            new_fileobj.write("* "+str(count)+"\n")
            count +=1
        
        num+=1
        if answer[int(line[0])] == line[1]: #予測した係り先文節IDが正解と一致しているか
            r+=1
        else:
            if int(answer[int(line[0])]) > count-1 and int(line[1]) < 0:    #正解の係り先が未入力 かつ 予測した係り先が未入力
                r+=1
                mi+=1
            else:   #不正解
                f+=1
                p=False
                data = " ".join(line)
                print(data)
                new_fileobj.write(data+"\n")
            
    if p:   #p=Trueなら文正解している
        br+=1
    
    new_fileobj.close()

print(f"文数　{n}")
print(f"文正解数　{br}")
print(f"文節数 {num}")
print(f"正解 {r}")
print(f"不正解 {f}")
print(f"係り先が未入力である文節の正解数　{mi}")