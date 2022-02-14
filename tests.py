# RANDOM TESTS
languages = []
languages.append("C++")
languages.append("HTML")
languages.append("Java")
languages.append("Ruby")

import gitlab_search as gls

first = gls.getFirstBackendLanguage(languages)
print(first)

l = gls.getBackendLanguages(languages)
print(l)