#AQUÍ irán las pruebas que se realicen.

#Importamos las librerías necesarias.
from github import Github
from github.GithubException import UnknownObjectException
import auxiliares as aux
import busqueda as b1
import datos as d
import herramientasCI as ci
# import openpyxl --> esta hay que instalarla en el venv para que funcione el generarEXCEL.

# Generamos un token para consultar la API de GitHub a través de la librería.
user = "jorcontrerasp"
token = aux.leerFichero("token")
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

    df = d.generarDataFrame(filteredRepos)
    d.generarEXCEL(df, "fExcelPruebas")

    files = ci.getFicherosBusquedaCI(ci.HerramientasCI.CI1.value)
    for file in files:
        print(str(file))

    aux.imprimirListaRepositorios(filteredRepos)
    listaEncontrados = b1.busquedaGitHubApiRepos(filteredRepos)

    print(str(len(listaEncontrados)))