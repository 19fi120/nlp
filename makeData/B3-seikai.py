import os
import glob

"""仕分け"""
path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjB"
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
    elif ('B1-seikai.dat' in file):
        pass
    elif ('B1-matigai.dat' in file):
        pass
    elif ('B2-seikai.dat' in file):
        pass
    elif ('B2-matigai.dat' in file):
        pass
    elif ('B3-seikai.dat' in file):
        pass
    elif ('B3-matigai.dat' in file):
        pass
    elif ('B4-seikai.dat' in file):
        pass
    elif ('B4-matigai.dat' in file):
        pass
    elif ('B4-NoEntry.dat' in file):
        pass
    elif ('B5-seikai.dat' in file):
        pass
    elif ('B5-matigai.dat' in file):
        pass
    elif ('B5-NoEntry.dat' in file):
        pass
    else:
        answerlist.append(file)

"""作成するファイル名"""
new_filelist = []   #分析のために作成するファイル名のリスト
for i,path in enumerate(dirs3):
    new_filelist.append(path+"/B3-seikai.dat")

"""得点表"""
def pointhyou(karilist,answer):
    dictlist = []
    for minyuryokuid in range(-1,-1*len(answer)-1,-1):
        pointlist = [0]*(len(answer)+1)
        for i,line in enumerate(karilist):
            if int(line[1]) == minyuryokuid:
                pointlist[int(answer[int(line[0])])] += 1
        
        for seikaiid in range(len(answer)+1):
            dictlist.append(((minyuryokuid,seikaiid),pointlist[seikaiid]))
            
    pointdict = dict(dictlist)
    return pointdict

"""動的計画法を利用した計算"""
def calc(bunid,answerNum,setMin,pointdict):
    celldict = {}   #{(セルの位置):[{(対応付けするセルの位置),...},合計得点],...}
    answerdict = {} #{未入力文節ID:対応付ける正解の係り先文節ID,...}
    
    for mi in range(-1,setMin-1,-1):        #mi = 未入力文節ID
        for si in range(bunid,answerNum):   #si = 正解の係り先文節ID
            #このセルのパラメータ
            cellposition = (mi,si)  #現在注目しているセルの位置
            taiou = set()   #このセルの対応付け
            point = pointdict[cellposition] #このセルの得点
            if point > 0:   #このセルに得点があるなら対応付けに加える
                taiou.add(cellposition)
            
            cell = set()
            cellp = 0
            
            #左のセル
            try:
                cell = celldict[(mi+1,si)][0]
                cellp = celldict[(mi+1,si)][1]
            except:
                pass
            
            #下のセル
            try:
                if cellp < celldict[(mi,si-1)][1]:
                    cell = celldict[(mi,si-1)][0]
                    cellp = celldict[(mi,si-1)][1]
            except:
                pass
            
            #左下のセル
            try:
                if cellp <= celldict[(mi+1,si-1)][1] + point:
                    cell = celldict[(mi+1,si-1)][0]
                    cell.add(cellposition)
                    cellp = celldict[(mi+1,si-1)][1] + point
            except:
                pass
            
            if point <= cellp:
                taiou = cell
                point = cellp
            
            celldict[cellposition] = [set(),point]
            for ta in taiou:
                celldict[cellposition][0].add(ta)
            
    for t in celldict[(setMin,answerNum-1)][0]:
        answerdict[t[0]] = t[1]
     
    return answerdict

n = 0   #文数
br = 0  #文正解の数
num = 0 #文節数
r = 0   #正解の数
f = 0   #不正解の数

p = True    #文正解数を数えるための変数
idnum = 0   #文節数を数えるための変数

for i,file in enumerate(filelist):
    #if file.count("950104")>0:
        #continue
    
    n += 1
    p = True
    
    """正解データのリストを作る"""
    answer = [] #["0文節目の正解の係り先文節ID","1文節目の正解の係り先文節ID",...]
    with open(answerlist[i],"r",encoding="utf_8") as fileobj:
        for a,line in enumerate(fileobj) :            
            if line.find("*") == 0:
                aline = line.rstrip()
                datalist = aline.split(" ")
                s = datalist[2]
                answer.append(s[:-1])

    """文節ごとの作業結果のリストを作る"""
    bunsetsulist = []   #[["文節ID","予測した係り先文節ID","得点"],...,["未入力文節ID","対応する正解の文節ID","予測した文字列","得点"],...]
    with open(file,"r",encoding="utf_8") as fileobj:
        for b,line in enumerate(fileobj) :            
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
    
    """現在表示された文節数"""
    count = 0   #何文節目までが既入力となっているかを示す
    karilist = []   #係り先が未入力の文節をまとめるための仮のリスト
    minyuuryoku_set = set() #未入力文節IDをまとめるためのセット
    for c,line in enumerate(bunsetsulist) :
        if int(line[0]) < -1:   #係り先が未入力の文節については、line[0]=-1の時にまとめてやる
            continue
        
        if int(line[0]) == 0:   #既入力の文節が追加される
            print("*",count)
            new_fileobj.write("* "+str(count)+"\n")
            count +=1
            karilist = []
            minyuuryoku_set = set()
            
        if int(line[0]) == -1:  #係り先が未入力の文節について、ここでまとめてやる
            if len(minyuuryoku_set) == 0:   #文末なので終了
                break
            answerdict = calc(count,len(answer),min(minyuuryoku_set),pointhyou(karilist,answer))
            for d,l in enumerate(karilist):
                try:
                    if int(answer[int(l[0])]) == answerdict[int(l[1])]: #正解の係り先文節IDと対応付けした文節IDか一致しているか
                        r+=1
                        data = " ".join(l)
                        print(data)
                        new_fileobj.write(data+"\n")
                    else:
                        f+=1
                        p=False
                except: #未入力文節IDが正解の係り先文節IDと対応付けされなかった場合
                    f+=1
                    p=False
            continue
        
        num+=1
        if answer[int(line[0])] == line[1]:
            r+=1
            data = " ".join(line)
            print(data)
            new_fileobj.write(data+"\n")
        else:
            if int(line[1]) < 0:    #係り先が未入力なら
                if int(answer[int(line[0])]) > count-1: #正解の係り先が未入力なら
                    karilist.append(line)   #評価を保留、line[0]=-1の時にやる
                    minyuuryoku_set.add(int(line[1]))
                else:   #不正解
                    f+=1
                    p=False
            else:   #不正解
                f+=1
                p=False
            
    """文正解数のカウント"""
    if p:
        br+=1
        
    new_fileobj.close()

print(f"文数　{n}")
print(f"文正解数　{br}")
print(f"文節数 {num}")
print(f"正解 {r}")
print(f"不正解 {f}")