#AQUÍ irán las pruebas que se realicen.

#Importamos las librerías necesarias.
from github import Github
from github.GithubException import UnknownObjectException
import auxiliares as aux
import datos as d
import herramientasCI as ci
import github_search as ghs
# import openpyxl --> esta hay que instalarla en el venv para que funcione el generarEXCEL.

# Generamos un github_token para consultar la API de GitHub a través de la librería.
user = "jorcontrerasp"
token = aux.readFile("tokens/github_token.txt")
g = Github(user, token)

organizacion = "envoyproxy"
repo = "envoy"

continuar = True

try:
    repo = g.get_repo(organizacion + "/" + repo)
except UnknownObjectException as e:
    print("El repositorio " + organizacion + "/" + repo + " no existe en GitHub: " + str(e))
    continuar = False

if continuar:
    print("Continuar con el proceso.")

    filteredRepos = [repo]

    df = d.makeDataFrame(filteredRepos, True)
    df2 = d.makeCounterDataFrame()

    files = ci.getCISearchFiles(ci.HerramientasCI.CI11.value)
    for file in files:
        print(str(file))

    aux.imprimirListaRepositorios(filteredRepos)

    listaEncontrados = []
    listaEncontrados = ghs.searchReposGitHubApi(filteredRepos, df, df2)

    d.makeEXCEL(df, "fExcelPruebas")
    d.makeEXCEL(df2, "fExcelPruebas2")

    print(str(len(listaEncontrados)))