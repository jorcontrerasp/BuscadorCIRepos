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
    if d.existsDFRecord("EmptyRecord",df):
        print("EXISTE")
    else:
        print("NO EXISTE")

    if d.existsDFRecord("AAA",df):
        print("EXISTE")
    else:
        print("NO EXISTE")
except:
    print("ERROR")