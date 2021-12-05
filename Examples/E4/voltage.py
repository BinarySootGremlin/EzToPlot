import numpy as num

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1


def get_uncert(U):
    res=0
    if(U<=4):
        res = 0.0001
    elif(U<=40):
        res = 0.001
    else:
        res = 0.01

    return (U/100)*0.5+res*40

filelist = ["dataset05_lks.ini", "dataset05_flo.ini"]

names = ["Spule: ","Kondensator: ","LC: ","Gen: ","RP: "]

for index,file in enumerate(filelist):

    pre_text = ""

    if index == 0:
        pre_text = "xxx: "
    else:
        pre_text = "yyy: "

    data_01 = []

    filename = file[file.rfind("\\")+1:]
    filename = filename[0:filename.find(".")]

    clean_values = []
    with open(file) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                data_01.append(float(value.rstrip()))

    for i, value in enumerate(data_01):
        print("%s %s (%f +/- %f) V" % (pre_text,names[i], value, get_uncert(value)))