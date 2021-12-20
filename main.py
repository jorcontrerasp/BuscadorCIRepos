#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import dataF_functions as d
import github_search as ghs
import gitlab_search as gls
import aux_functions as aux
import pandas as pd
import os
import logging
import yaml_parser as ymlp

# Configuración del proceso de búsqueda.
config = "process"
execute = ymlp.parseConfigParam(config, "execute")
doGithubSearch = ymlp.parseConfigParam(config, "doGithubSearch")
doGitlabSearch = ymlp.parseConfigParam(config, "doGitlabSearch")
usePickleFile = ymlp.parseConfigParam(config, "usePickleFile")
useResultsExcelFile = ymlp.parseConfigParam(config, "useResultsExcelFile")

def executeProcess():
    try:
        aux.printLog("Iniciando proceso...", logging.INFO)
        fRepos = ""

        # Generamos un DataFrame donde irán los contadores.
        fCount = "results/contadores.xlsx"
        if useResultsExcelFile:
                if os.path.exists(fCount):
                    counterDF = pd.read_excel(fCount, index_col=0)
                else:
                    counterDF = d.makeCounterDataFrame()
        else:
            counterDF = d.makeCounterDataFrame()

        if doGithubSearch:

            fRepos = "github_repos.pickle"
            fResults = "results/resultados_github.xlsx"

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
            # githubDF = d.makeDataFrame(lFinal, True)
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    githubDF = pd.read_excel(fResults, index_col=0)
                else:
                    githubDF = d.makeEmptyDataFrame()
            else:
                githubDF = d.makeEmptyDataFrame()

            # Aplicamos el proceso.
            lFound = []
            lFound = ghs.searchReposGitHubApi(lFinal, githubDF, counterDF)

        if doGitlabSearch:

            fRepos = "gitlab_repos.pickle"
            fResults = "results/resultados_gitlab.xlsx"

            lFound = []
            lResult = []

            # Generamos un DataFrame donde irán los resultados.
            # gitlabDF = d.makeDataFrame(lFinal, False)
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    gitlabDF = pd.read_excel(fResults, index_col=0)
                else:
                    gitlabDF = d.makeEmptyDataFrame()
            else:
                gitlabDF = d.makeEmptyDataFrame()
            
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitLab.", logging.INFO)
                if os.path.exists(fRepos):
                    lFinal = aux.loadRepositories(fRepos)

                    # Aplicamos el proceso.
                    lFound = gls.searchInProjectsGitLabApi(lFinal, gitlabDF, counterDF)

                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                lFound,lResult = gls.doSearchGitLabApi(gitlabDF, counterDF)
            
        # Generamos un fichero EXCEL con los contadores.
        d.makeEXCEL(counterDF, "contadores")

        aux.printLog("Proceso finalizado.", logging.INFO)

    except:
        aux.printLog("Se ha producido un ERROR inesperado.", logging.ERROR)
        raise
        # FIN

if execute:
    executeProcess()