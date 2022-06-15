import subprocess
import os
import glob

"""ファイル仕分け"""
path = "../HumanIncreParse/HumanIncreParse/HumanIncreParse/SubjA"
dirs1 = []  # 年月日
dirs1 = glob.glob(os.path.join(path, '*'))
dirs2 = []  # 記事番号
for i, path2 in enumerate(dirs1):
    dirs2 += glob.glob(os.path.join(path2, '*'))
dirs3 = []  # 記事の文番号
for i, path3 in enumerate(dirs2):
    dirs3 += glob.glob(os.path.join(path3, '*'))
datlist = []
for i, path4 in enumerate(dirs3):
    datlist += glob.glob(os.path.join(path4, '*.dat'))

filelist = []
for i, file in enumerate(datlist):
    if ('result.dat' in file):
        filelist.append(file)

"""jumanのファイル"""
new_filelist = []
for i, path in enumerate(dirs3):
    new_filelist.append(path + "/juman.dat")

"""JUMAN"""
def juman(str):
    cmd = "juman"
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    proc.communicate(str.encode('cp932'))

    repr = proc.communicate()
    line = repr[0].decode('cp932').split("\r\n")

    tmp = []
    for i, l in enumerate(line):
        aline = l.rstrip()
        datalist = aline.split(" ")
        tmp.append(datalist)

    jiritugo = []
    for i, l in enumerate(tmp):
        if len(l) != 1:
            if l[3] != "助詞" and l[3] != "助動詞" and l[3] != "特殊" and l[3] != "接尾辞" and l[0] != "@":
                jiritugo.append(l[0])

    proc.terminate()
    return jiritugo


"""ファイルを作成する"""
for i, file in enumerate(filelist):

    bunsetsulist = []
    with open(file, "r", encoding="utf_8") as fileobj:
        for z, line in enumerate(fileobj):
            if line.count("#") > 0:
                continue
            if line.count("*") > 0:
                continue
            aline = line.rstrip()
            datalist = aline.split(" ")
            bunsetsulist.append(datalist)

    new_fileobj = open(new_filelist[i], "w", encoding="shift_jis")
    print(new_filelist[i])

    for x, line in enumerate(bunsetsulist):
        if int(line[0]) >= 0:
            new_fileobj.write("\n")
            continue

        if len(line[2]) <= 0:
            new_fileobj.write("\n")
            continue
        else:
            j_list = juman(line[2])
            j = ""  # 形態素毎
            jrt = ""  # 自立語まとめて
            for y, a in enumerate(j_list):
                j += a
                j += " "
                jrt += a

        print(j + jrt)
        new_fileobj.write(j + jrt + "\n")

    new_fileobj.close()