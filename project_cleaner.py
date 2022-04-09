import aux_functions as aux
import gitlab_search as gls
import ci_yml_parser as ymlp
import shutil
from shutil import rmtree
import os

doCleanProject = True
config = "process"
tmpDirectory = ymlp.parseConfigParam(config, "tmpDirectory")
tmpFile = tmpDirectory + ymlp.parseConfigParam(config, "tmpFile")

#CONFIGURACIÓN DEL BORRADO DE FICHEROS
deletePickles = True
deleteResults = True
deleteTmpFiles = True
deleteLogs = True
deleteLaTeX = True

def cleanProject():
    try:
        print("Limpiando proyecto...")

        #ELIMINAR CARPETAS Y FICHEROS BASURA
        if deleteTmpFiles and os.path.exists(tmpDirectory):
            rmtree("./" + tmpDirectory)
        if deleteResults and os.path.exists("results"):
            rmtree("results")
        if deleteLogs and os.path.exists("logs"):
            rmtree("logs")
        if deleteLogs and os.path.exists("LaTeX"):
            rmtree("LaTeX")
        if deletePickles and os.path.exists("github_repos.pickle"):
            os.remove("github_repos.pickle")
        if deletePickles and os.path.exists("gitlab_repos.pickle"):
            os.remove("gitlab_repos.pickle")

        #CREAR CARPETAS
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists("logs"):
            os.mkdir("logs")
        if not os.path.exists("LaTeX"):
            os.mkdir("LaTeX")

        print("Proceso terminado...")
    except:
        raise

if doCleanProject:
    cleanProject()