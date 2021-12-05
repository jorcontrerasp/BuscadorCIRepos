#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import dataF_functions as d
import github_search as ghs
import gitlab_search as gls
import aux_functions as aux
import os
import logging

execute = True
doGithubSearch = True
doGitlabSearch = True
usePickleFile = False

def executeProcess():
    try:
        aux.printLog("Iniciando proceso...", logging.INFO)
        fRepos = ""

        # Generamos un DataFrame donde irán los contadores.
        counterDF = d.makeCounterDataFrame()

        if doGithubSearch:
            fRepos = "github_repos.pickle"
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitHub.", logging.INFO)
                if os.path.exists(fRepos):
                    lFinal = aux.loadRepositories(fRepos)
                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                # Obtenemos la lista de repositorios Github.
                lFinal = ghs.getGithubRepos()

            # Generamos un DataFrame donde irán los resultados.
            #githubDF = d.makeDataFrame(lFinal, True)
            githubDF = d.makeEmptyDataFrame()

            # Aplicamos el proceso.
            lFound = []
            lFound = ghs.searchReposGitHubApi(lFinal, githubDF, counterDF)

        if doGitlabSearch:
            fRepos = "gitlab_repos.pickle"
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitLab.", logging.INFO)
                if os.path.exists(fRepos):
                    lFinal = aux.loadRepositories(fRepos)
                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                # Obtenemos la lista de repositorios Gitlab.
                lFinal = gls.getGitlabProjects()

            # Generamos un DataFrame donde irán los resultados.
            #gitlabDF = d.makeDataFrame(lFinal, False)
            gitlabDF = d.makeEmptyDataFrame()

            # Aplicamos el proceso.
            lFound = []
            lFound = gls.searchProjectsGitLabApi(lFinal, gitlabDF, counterDF)
            
        # Generamos un fichero EXCEL con los contadores.
        d.makeEXCEL(counterDF, "contadores")

        aux.printLog("Proceso finalizado.", logging.INFO)

    except:
        aux.printLog("Se ha producido un ERROR inesperado.", logging.ERROR)
        raise
        # FIN

if execute:
    executeProcess()