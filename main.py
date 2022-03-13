#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import dataF_functions as d
import github_search as ghs
import gitlab_search as gls
import aux_functions as aux
import ci_yml_parser as ymlp
import pandas as pd
import os
import logging

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
            fResults = "results/github/github_results.xlsx"
            fLanguages = "results/github/github_languages.xlsx"
            fStageStatistics = "results/github/github_stage_statistics.xlsx"

            # Generamos un DataFrame donde irán los resultados.
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    githubDF = pd.read_excel(fResults, index_col=0)
                    githubLanguagesDF = pd.read_excel(fLanguages, index_col=0)
                    githubStageStatisticsDF = pd.read_excel(fStageStatistics, index_col=0)
                else:
                    githubDF = d.makeEmptyDataFrame()
                    githubLanguagesDF = d.makeEmptyLanguageDataFrame()
                    githubStageStatisticsDF = d.makeEmptyStageStatisticsDataFrame()
            else:
                githubDF = d.makeEmptyDataFrame()
                githubLanguagesDF = d.makeEmptyLanguageDataFrame()
                githubStageStatisticsDF = d.makeEmptyStageStatisticsDataFrame()
                
            # Obtenemos la lista de repositorios Github.
            lFound = ghs.getGithubRepos(usePickleFile)

            # Aplicamos el proceso.
            lResult = []
            lResult = ghs.searchReposGitHubApi(lFound, githubDF, counterDF, githubLanguagesDF, githubStageStatisticsDF)

        if doGitlabSearch:
            fRepos = "gitlab_repos.pickle"
            fResults = "results/gitlab/gitlab_results.xlsx"
            fLanguages = "results/gitlab/gitlab_languages.xlsx"
            fStageStatistics = "results/gitlab/gitlab_stage_statistics.xlsx"

            lFound = []
            lResult = []

            # Generamos un DataFrame donde irán los resultados.
            if useResultsExcelFile:
                if os.path.exists(fResults):
                    gitlabDF = pd.read_excel(fResults, index_col=0)
                    gitlabLanguagesDF = pd.read_excel(fLanguages, index_col=0)
                    gitlabStageStatisticsDF = pd.read_excel(fStageStatistics, index_col=0)
                else:
                    gitlabDF = d.makeEmptyDataFrame()
                    gitlabLanguagesDF = d.makeEmptyLanguageDataFrame()
                    gitlabStageStatisticsDF = d.makeEmptyStageStatisticsDataFrame()
            else:
                gitlabDF = d.makeEmptyDataFrame()
                gitlabLanguagesDF = d.makeEmptyLanguageDataFrame()
                gitlabStageStatisticsDF = d.makeEmptyStageStatisticsDataFrame()
            
            if usePickleFile:
                aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitLab.", logging.INFO)
                if os.path.exists(fRepos):
                    lFound = aux.loadRepositories(fRepos)

                    # Aplicamos el proceso.
                    lResult = gls.searchInProjectsGitLabApi(lFound, gitlabDF, counterDF, gitlabLanguagesDF, gitlabStageStatisticsDF)

                else:
                    raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
            else:
                lFound,lResult = gls.doSearchGitLabApi(gitlabDF, counterDF, gitlabLanguagesDF, gitlabStageStatisticsDF)
            
        # Generamos un fichero EXCEL con los contadores.
        d.makeEXCEL(counterDF, "counting")

        aux.printLog("Proceso finalizado.", logging.INFO)

    except:
        aux.printLog("Se ha producido un ERROR inesperado.", logging.ERROR)
        raise
        # FIN

if execute:
    executeProcess()