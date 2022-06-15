import os
import glob

"""仕分け"""
path = "../HumanIncreParse_SIDB/HumanIncreParse_SIDB"
dirs1 = []  #シンポジウム番号
dirs1 = glob.glob(os.path.join(path, '*'))
dirs2 = []  #シンポジウムの文番号
for i,path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
datlist = []#datファイルのリスト
for i,path3 in enumerate(dirs2):
    datlist += glob.glob(os.path.join(path3,'*.dat'))
    
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

"""得点表"""
def pointhyou(karilist,answer):
    dictlist = []
    for minyuryokuid in range(-1,-1*len(answer)-1,-1):
        pointlist = [0]*(len(answer)+1)
        for i,line in enumerate(karilist):
            if int(line[1]) == minyuryokuid:
                pointlist[int(answer[int(line[0])][0])] += 1
        
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

mia = 0 #正解の係り受け構造において未入力の係り先となる文節の数
mo = 0  #何らかの文字列を予測した未入力係り先文節の数

mNum = 0    #未入力の係り先の個数
kanzen = 0  #文字列を完全に予測した数
tigau = 0   #文字列を完全に予測できなかった数
NE = 0      #文字を入力していない個数

for i,file in enumerate(filelist):
    """論文にないデータを除く"""
    #if file.count("950104")>0:
        #continue
    
    n += 1
    p = True
    
    """正解データのリストを作る"""
    answer = [] #[["0文節目の正解の係り先文節ID","正解の文字列"],...]
    with open(answerlist[i],"r",encoding="utf_8") as fileobj:
        tmp = []
        text = ""
        for a,line in enumerate(fileobj) :  
            if line.count("#") > 0:
                continue
            if line.count("EOS") > 0:
                break
            
            aline = line.rstrip()
            datalist = aline.split(" ")
            
            if line.find("*") == 0:
                if text != "":
                    tmp.append(text)
                    text = ""
                if len(tmp) != 0 : 
                    answer.append(tmp)
                    tmp = []
                s = datalist[2]
                tmp.append(s[:-1])
            else:
                text += datalist[0]
        tmp.append(text)
        answer.append(tmp)

    """文節ごとの作業結果のリストを作る"""
    bunsetsulist = []   #[["文節ID","予測した係り先文節ID","得点"],...,["未入力文節ID","対応する正解の文節ID","予測した文字列","得点"],...]
    with open(file,"r",encoding="utf_8") as fileobj:
        for a,line in enumerate(fileobj) :            
            if line.count("#")>0:
                continue
            if line.count("*")>0:
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            bunsetsulist.append(datalist)
    
    """現在表示された文節数"""
    count = 0   #何文節目までが既入力となっているかを示す
    karilist = []   #係り先が未入力の文節をまとめるための仮のリスト
    minyuuryoku_set = set() #未入力文節IDをまとめるためのセット
    answerdict = {} #未入力係り先文節IDと正解の文節IDを対応付けた辞書
    
    for b,line in enumerate(bunsetsulist) :
        if int(line[0]) == 0:   #既入力の文節が追加される
            count +=1
            karilist = []
            minyuuryoku_set = set()
            mi_set = set()  #miaを数えるためのセット
            for c in range(count):
                if int(answer[c][0]) >= count and int(answer[c][0]) != -1:
                    mi_set.add(int(answer[c][0]))
            mia += len(mi_set)
            exNum = 0   #未入力係り先文節が正解と対応付けされてないときに、それを区別するためのID
            
        if int(line[0]) == -1:
            if len(minyuuryoku_set) == 0:
                break
            mNum += len(minyuuryoku_set)
            answerdict = calc(count,len(answer),min(minyuuryoku_set),pointhyou(karilist,answer))
            for d,l in enumerate(karilist): #係り受けの評価
                try:
                    if int(answer[int(l[0])][0]) == answerdict[int(l[1])]:
                        r+=1
                    else:
                        f+=1
                        p=False
                except:
                    f+=1
                    p=False
            
            if int(line[0]) in minyuuryoku_set: #文字列の評価、ifの条件などはこのプログラムの一番下
                if len(line[2]) > 0:
                    mo += 1
                    try:
                        if answer[answerdict[int(line[0])]][1] == line[2]:
                            kanzen += 1
                        else:
                            tigau += 1
                    except:
                        tigau += 1
                else:
                    NE += 1
            else:
                pass
            continue
        
        if int(line[0]) < -1:   #文字列の評価、ifの条件などはこのプログラムの一番下
            if int(line[0]) in minyuuryoku_set:
                if len(line[2]) > 0:
                    mo += 1
                    try:
                        if answer[answerdict[int(line[0])]][1] == line[2]:
                            kanzen += 1
                        else:
                            tigau += 1
                    except:
                        tigau += 1
                else:
                    NE += 1
            else:
                pass
            continue
        
        num+=1
        if answer[int(line[0])][0] == line[1]:
            r+=1
        else:
            if int(line[1]) < 0:    #係り先が未入力なら
                if int(answer[int(line[0])][0]) > count-1:  #正解の係り先が未入力なら
                    karilist.append(line)   #評価を保留、line[0]=-1の時にやる
                    minyuuryoku_set.add(int(line[1]))
                else:
                    f+=1
                    p=False
            else:
                f+=1
                p=False
            
    """文正解数のカウント"""
    if p:
        br+=1

print(f"文数　{n}")
print(f"文正解数　{br}")
print(f"文節数 {num}")
print(f"正解 {r}")
print(f"不正解 {f}")
print(f"正解の係り受け構造において未入力の係り先となる文節の数 {mia}")
print(f"何らかの文字列を予測した未入力係り先文節の数 {mo}")
print(f"未入力の係り先の個数 {mNum}")
print(f"文字列を完全に予測した数 {kanzen}")
print(f"文字列を完全に予測できなかった数 {tigau}")
print(f"文字を入力していない個数 {NE}")

"""
↓文字列の評価プログラム

未入力係り先文節であるか
    文字列が入力されているか
        文字列が一致している    ←正解
        文字列が一致していない  ←不正解
        対応する文節がない     ←対象外
    文字が入力されていない      ←未入力
未入力係り先文節でない
    文字が入力されている
"""