#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import datos as d
import github_search as ghs
import gitlab_search as gls
import auxiliares as aux
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
            githubDF = d.makeDataFrame(lFinal, True)

            # Generamos un DataFrame donde irán los contadores.
            githubDF2 = d.makeCounterDataFrame()

            # Aplicamos el proceso.
            lFound = []
            lFound = ghs.searchReposGitHubApi(lFinal, githubDF, githubDF2)

            # Generamos un fichero EXCEL con los resultados.
            d.makeEXCEL(githubDF, "resultados_github")

            # Generamos un fichero EXCEL con los contadores.
            d.makeEXCEL(githubDF2, "contadores_github")

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
                lFinal = gls.getGitlabProyects()

            # Generamos un DataFrame donde irán los resultados.
            gitlabDF = d.makeDataFrame(lFinal, False)

            # Generamos un DataFrame donde irán los contadores.
            gitlabDF2 = d.makeCounterDataFrame()

            # Aplicamos el proceso.
            listaEncontrados = []
            listaEncontrados = gls.searchProyectsGitLabApi(lFinal, gitlabDF, gitlabDF2)

            # Generamos un fichero EXCEL con los resultados.
            d.makeEXCEL(gitlabDF, "resultados_gitlab")

            # Generamos un fichero EXCEL con los contadores.
            d.makeEXCEL(gitlabDF2, "contadores_gitlab")

        aux.printLog("Proceso finalizado.", logging.INFO)

    except:
        aux.printLog("Se ha producido un ERROR inesperado.", logging.ERROR)
        raise
        # FIN

if execute:
    executeProcess()