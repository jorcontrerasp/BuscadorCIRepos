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
# AMAI-GmbH/AI-Expert-Roadmap 
# jwasham/coding-interview-university
# gztchan/awesome-design
# agalwood/motrix
# kr328/clashforandroid
# salomonelli/best-resume-ever
# facebook/create-react-app
# goldbergyoni/nodebestpractices
# freecad/freecad
# vuejs/core
# artf/grapesjs
repoName = "vuejs/core"
doTest = True
doSearchInAllCiTools = True

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
        d.makeEXCEL(df2, "_counting")
    else:
        found,df,df3,df6 = ghs.searchLiteralPathFromRoot(repo, ciTool, df, df2, df3, df6)
        #found,df,df3,df6 = ghs.searchLiteralPathFromRoot_REC(repo, ciTool, [], df, df2, df3, df6, [])
        df,df2,df4,df5 = d.doAuxWithResultsDF(df, df2, df3, True)

        d.makeEXCEL(df, "github/_github_results")
        d.makeEXCEL(df2, "github/_counting")
        d.makeEXCEL(df3, "github/_github_languages")
        d.makeEXCEL(df4, "github/_github_language_statistics")
        d.makeEXCEL(df5, "github/_github_ci_statistics")
        d.makeEXCEL(df6, "github/_gitlab_stage_statistics")

print("Fin de la prueba.")