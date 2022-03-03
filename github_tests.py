#AQUÍ irán las pruebas que se realicen sobre GitHub.

#Importamos las librerías necesarias.
from github import Github
from github.GithubException import UnknownObjectException
import aux_functions as aux
import dataF_functions as d
import ci_tools as ci
import github_search as ghs
# import openpyxl --> esta hay que instalarla en el venv para que funcione el generarEXCEL.

# Generamos un github_token para consultar la API de GitHub a través de la librería.
user = "jorcontrerasp"
token = aux.readFile("tokens/github_token.txt")
g = Github(user, token)

ciTool = ci.HerramientasCI.CI2
# zhihu/Matisse
# EOSIO/eos
repoName = "EOSIO/eos"
doTest = True
doSearchInAllCiTools = False

try:
    repo = g.get_repo(repoName)
except UnknownObjectException as e:
    print("El repositorio " + repoName + " no existe en GitHub: " + str(e))
    doTest = False

if doTest:

    filteredRepos = [repo]

    df = d.makeDataFrame(filteredRepos, True)
    df2 = d.makeCounterDataFrame()
    df3 = d.makeEmptyLanguageDataFrame()
    df6 = d.makeEmptyStageStatisticsDataFrame()

    if doSearchInAllCiTools:
        foundList = []
        foundList = ghs.searchReposGitHubApi(filteredRepos, df, df2, df3, df6)
    else:
        found,df,df3,df6 = ghs.searchLiteralPathFromRoot2(repo, ciTool, df, df2, df3, df6)
        d.makeEXCEL(df, "_github_results")
        d.makeEXCEL(df2, "_counting")
        d.makeEXCEL(df3, "_github_languages")
        d.makeEXCEL(df6, "_gitlab_stage_statistics")

print("Fin de la prueba.")