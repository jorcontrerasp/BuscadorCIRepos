# RANDOM TESTS
languages = []
languages.append("C++")
languages.append("HTML")
languages.append("Java")
languages.append("Ruby")

import gitlab_search as gls
import dataF_functions as d

first = gls.getFirstBackendLanguage(languages)
print(first)

l = gls.getBackendLanguages(languages)
print(l)

df = d.makeEmptyDataFrame()
try:
    if d.existsDFRecord("pd_empty_record",df):
        print("EXISTE")
    else:
        print("NO EXISTE")

    if d.existsDFRecord("AAA",df):
        print("EXISTE")
    else:
        print("NO EXISTE")
except:
    print("ERROR")

aaa = dict()
aaa["aaa aaa"] = "aaa"
print(aaa)
bbb = aaa.keys()
print(bbb)

ccc = aaa["aaa aaa"]
print(ccc)

lista = [1, 2, 3, 4, 5]
for i in lista:
    if i == 3:
        continue
    print(i)

l = [["a", "b", "c"], ["r"]]

i = 0
for topLevel in l:
    stage = "aaa"
    if i == 1:
        stage = ""
    whenAux = topLevel
    lWhen = []
    lWhenStages = []
    if isinstance(whenAux, list) or isinstance(whenAux, dict):
        for wAux in whenAux:
            lWhen.append(wAux)
    else:
        lWhen.append(whenAux)

    if len(stage)>0:
        if len(lWhen)>0:
            for lw in lWhen:
                lWhenStages.append(stage + ">" + lw)
        else:
            lWhenStages.append(stage)
    else:
        if len(lWhen)>0:
            for lw in lWhen:
                lWhenStages.append("script" + ">" + lw)
        else:
            lWhenStages.append("script")
    i = i+1

    print(lWhenStages)