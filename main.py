#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import dataF_functions as d
import github_search as ghs
import gitlab_search as gls
import aux_functions as aux
import pandas as pd
import os
import logging
import ci_yml_parser as ymlp

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
        fCount = "results/counting.xlsx"
        if useResultsExcelFile:
                if os.path.exists(fCount):
                    counterDF = pd.read_excel(fCount, index_col=0)
                else:
                    counterDF = d.makeCounterDataFrame()
        else:
            counterDF = d.makeCounterDataFrame()

        if doGithubSearch:

            fRepos = "github_repos.pickle"
            fResults = "results/github_results.xlsx"
            fLanguages = "results/github_languajes.xlsx"

            # Generamos un DataFrame donde irán los resultados.
            # githubDF = d.makeDataFrame(lFinal, True)
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    githubDF = pd.read_excel(fResults, index_col=0)
                    githubLanguagesDF = pd.read_excel(fLanguages, index_col=0)
                else:
                    githubDF = d.makeEmptyDataFrame()
                    githubLanguagesDF = d.makeEmptyLanguageDataFrame()
            else:
                githubDF = d.makeEmptyDataFrame()
                githubLanguagesDF = d.makeEmptyLanguageDataFrame()
                
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitHub.", logging.INFO)
                if os.path.exists(fRepos):
                    
                    lFound = aux.loadRepositories(fRepos)
                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                # Obtenemos la lista de repositorios Github.
                lFound = ghs.getGithubRepos()

            # Aplicamos el proceso.
            lResult = []
            lResult = ghs.searchReposGitHubApi(lFound, githubDF, counterDF, githubLanguagesDF)

        if doGitlabSearch:
            fRepos = "gitlab_repos.pickle"
            fResults = "results/gitlab_results.xlsx"
            fLanguages = "results/gitlab_languages.xlsx"

            lFound = []
            lResult = []

            # Generamos un DataFrame donde irán los resultados.
            # gitlabDF = d.makeDataFrame(lFinal, False)
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    gitlabDF = pd.read_excel(fResults, index_col=0)
                    gitlabLanguageDF = pd.read_excel(fLanguages, index_col=0)
                else:
                    gitlabDF = d.makeEmptyDataFrame()
                    gitlabLanguageDF = d.makeEmptyLanguageDataFrame()
            else:
                gitlabDF = d.makeEmptyDataFrame()
                gitlabLanguageDF = d.makeEmptyLanguageDataFrame()
            
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitLab.", logging.INFO)
                if os.path.exists(fRepos):
                    lFound = aux.loadRepositories(fRepos)

                    # Aplicamos el proceso.
                    lResult = gls.searchInProjectsGitLabApi(lFound, gitlabDF, counterDF, gitlabLanguageDF)

                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                lFound,lResult = gls.doSearchGitLabApi(gitlabDF, counterDF, gitlabLanguageDF)
            
        # Generamos un fichero EXCEL con los contadores.
        d.makeEXCEL(counterDF, "counting")

        aux.printLog("Proceso finalizado.", logging.INFO)

    except:
        aux.printLog("Se ha producido un ERROR inesperado.", logging.ERROR)
        raise
        # FIN

if execute:
    executeProcess()