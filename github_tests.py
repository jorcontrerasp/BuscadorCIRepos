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
organization = "OpenGenus"
repo = "cosmos"

continueTest = True

try:
    repo = g.get_repo(organization + "/" + repo)
except UnknownObjectException as e:
    print("El repositorio " + organization + "/" + repo + " no existe en GitHub: " + str(e))
    continueTest = False

if continueTest:
    print("Continuar con el proceso.")

    filteredRepos = [repo]

    df = d.makeDataFrame(filteredRepos, True)
    df2 = d.makeCounterDataFrame()
    df3 = d.makeEmptyLanguageDataFrame()

    files = ci.getCISearchFiles(ciTool.value)
    for file in files:
        print(str(file))

    aux.printGitHubRepoList(filteredRepos)

    foundList = []
    #foundList = ghs.searchReposGitHubApi(filteredRepos, df, df2, df3)

    found,df,df3 = ghs.searchLiteralPathFromRoot2(repo, ciTool, df, df2, df3)

    d.makeEXCEL(df, "fExcelPruebas")
    d.makeEXCEL(df2, "fExcelPruebas2")

    print(str(len(foundList)))