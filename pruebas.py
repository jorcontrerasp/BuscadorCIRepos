#AQUÍ irán las pruebas que se realicen.

#Importamos las librerías necesarias.
from github import Github
from github.GithubException import UnknownObjectException
import auxiliares as aux

# Generamos un token para consultar la API de GitHub a través de la librería.
user = "jorcontrerasp"
token = "AAA"
g = Github(user, token)

organizacion = "AAA"
repo = "BBB"

continuar = True

try:
    repo = g.get_repo(organizacion + "/" + repo)
except UnknownObjectException as e:
    print("El repositorio " + organizacion + "/" + repo + " no existe en GitHub: " + str(e))
    continuar = False

if continuar:
    print("Continuar con el proceso.")

    filteredRepos = [repo]

    aux.imprimirListaRepositorios(filteredRepos)