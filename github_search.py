#AQUÍ se implementará la búsqueda en GitHub.

#Importamos las librerías necesarias.
from github import Github
import aux_functions as aux
import ci_yml_parser as ymlp
import dataF_functions as d
import ci_tools as ci
import random
import logging
import calendar
import time
import datetime
import os
import requests
import json

# Configuración de la búsqueda GitHub.
config = "github"
queryFile = ymlp.parseConfigParam(config, "queryFile")
filterCommits = ymlp.parseConfigParam(config, "filterCommits")
MIN_COMMITS = ymlp.parseConfigParam(config, "MIN_COMMITS")
MAX_COMMITS = ymlp.parseConfigParam(config, "MAX_COMMITS")
randomizeRepos = ymlp.parseConfigParam(config, "randomizeRepos")
N_RANDOM = ymlp.parseConfigParam(config, "N_RANDOM")
onlyPositives = ymlp.parseConfigParam(config, "onlyPositives")

def authenticate():
    # Nos autenticamos y generamos un github_token para consultar la API de GitHub a través de la librería.
    user = "jorcontrerasp"
    token = aux.readFile("tokens/github_token.txt")
    g = Github(user, token)

    return g

def getGithubRepos(usePickleFile):
    fRepos = "github_repos.pickle"
    if usePickleFile:
        aux.printLog("Utilizando el fichero " + fRepos + " para generar los repositorios GitHub.", logging.INFO)
        if os.path.exists(fRepos):
            filteredRepos = aux.loadRepositories(fRepos)
        else:
            raise Exception("No se ha encontrado el fichero pickle en la raíz del proyecto.")
    else:
        g = authenticate()

        q = aux.readFile(queryFile)
        #query = mq.mGithubQuery.getQueryIni()
        aux.printLog("Ejecutando query: " + queryFile, logging.INFO)
        generator = g.search_repositories(query=q)

        # Convertimos el generador en una lista de repositorios.
        aux.printLog("Generando lista de repositorios GitHub...", logging.INFO)
        repositories = list(generator)

        # Filtramos por el número de COMMITS.
        filteredRepos = []

        if filterCommits:
            for repo in repositories:
                commits = repo.get_commits().totalCount
                if commits >= MIN_COMMITS and commits <= MAX_COMMITS:
                    filteredRepos.append(repo)
        else:
            for repo in repositories:
                filteredRepos.append(repo)

    # Seleccionamos N repositorios de manera aleatoria:
    lFinal = []
    if randomizeRepos:
        while len(lFinal) < N_RANDOM:
            item = random.choice(filteredRepos)
            if item not in lFinal:
                lFinal.append(item)
    else:
        lFinal = filteredRepos

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    aux.makePickle(fRepos, lFinal)
    lFinal = aux.loadRepositories(fRepos)

    # Imprimimos la lista de repositorios
    aux.printGitHubRepoList(lFinal)
    aux.printLog("Nº de repositorios: " + str(len(lFinal)), logging.INFO)

    return lFinal

def getContents(repo, path):
    # Aplicamos el control de la API rate.
    doApiRateLimitControl()
    # Obtenemos el contenido del repo.
    contents = repo.get_contents(path)

    return contents

def doApiRateLimitControl():
    try:
        g = authenticate()
        rl = g.get_rate_limit()
        rl_core = rl.core
        core_remaining = rl_core.remaining
        rl_search = rl.search
        search_remaining = rl_search.remaining
        if core_remaining <= 0:
            reset_timestamp = calendar.timegm(rl_core.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 5
            print("API rate limit exceded: " + str(sleep_time) + " sleep_time. Waiting...")
            time.sleep(sleep_time)
            g = authenticate()
    except:
        aux.printLog("Error al aplicar el control del API rate limit exceded...", logging.ERROR)

def searchReposGitHubApi(lRepositories, df, df2, df3, df6):
    lFound = []
    for repo in lRepositories:

        if not onlyPositives and not d.existsDFRecord(repo.full_name, df):
            df = d.addDFRecord(repo, df, True)

        if d.existsDFRecord(repo.full_name, df):
            df = d.initCIYamlColumns(repo.full_name, df)

        #found1,df,df3,df6,lStagesProjectAdded = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI1, [], df, df2, df3, df6, [])
        #found2,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI2, [], df, df2, df3, df6, [])
        #found3,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI3, [], df, df2, df3, df6, [])
        #found4,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI4, [], df, df2, df3, df6, [])
        #found5,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI5, [], df, df2, df3, df6, [])
        #found6,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI6, [], df, df2, df3, df6, [])
        #found7,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI7, [], df, df2, df3, df6, [])
        #found8,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI8, [], df, df2, df3, df6, [])
        #found9,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI9, [], df, df2, df3, df6, [])
        #found10,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI10, [], df, df2, df3, df6, [])
        #found11,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI11, [], df, df2, df3, df6, [])
        #found12,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI12, [], df, df2, df3, df6, [])
        #found13,df,df3,df6,lStagesProjectAdded  = searchLiteralPathFromRoot_REC(repo, ci.HerramientasCI.CI13, [], df, df2, df3, df6, [])

        found1,df,df3,df6 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI1, df, df2, df3, df6)
        found2,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI2, df, df2, df3, df6)
        found3,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI3, df, df2, df3, df6)
        found4,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI4, df, df2, df3, df6)
        found5,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI5, df, df2, df3, df6)
        found6,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI6, df, df2, df3, df6)
        found7 = False #found7,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI7, df, df2, df3, df6)
        found8,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI8, df, df2, df3, df6)
        found9,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI9, df, df2, df3, df6)
        found10,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI10, df, df2, df3, df6)
        found11,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI11, df, df2, df3, df6)
        found12,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI12, df, df2, df3, df6)
        found13,df,df3,df6  = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI13, df, df2, df3, df6)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(repo)

    df,df2,df4,df5 = d.doAuxWithResultsDF(df, df2, df3, True)

    # Generamos ficheros EXCEL con los resultados.
    d.makeEXCEL(df, "github/github_results")
    d.makeEXCEL(df3, "github/github_languages")
    d.makeEXCEL(df4, "github/github_language_statistics")
    d.makeEXCEL(df5, "github/github_ci_statistics")
    d.makeEXCEL(df6, "github/github_stage_statistics")

    return lFound

def searchLiteralPathFromRoot_REC(repo, CITool, literals, df, df2, df3, df6, lStagesProjectAdded):
    aux.printLog("Buscando '" + CITool.value + "' en '" + repo.full_name + "'", logging.INFO)
    try:
        if len(literals)==0:
            literals = ci.getCISearchFiles(CITool.value)

        path = literals.pop(0)
        getContents(repo, path)

        if not d.existsDFRecord(repo.full_name, df):
            df = d.addDFRecord(repo, df, True)
            
        df = d.updateDataFrameCiColumn(repo, "***", CITool, True, df)
        df2 = d.add1CounterDFRecord(CITool.value.lower(), "Encontrados_GitHub", df2)

        language = "None"
        if len(str(repo.language)) > 0:
            language = str(repo.language)
        if not d.existsDFRecord(language, df3):
            df3 = d.addLanguageDFRecord(language, df3)
        
        df3 = d.add1CounterDFRecord(language.lower(), CITool.value, df3)

        # lStagesProjectAdded --> Lista de 'stages' a los que se les ha hecho un +1 en proyectos que lo utilizan.
        ciObjRes = ymlp.getParseObj(repo, path, CITool, True)
        if isinstance(ciObjRes, list):
            for ciObj in ciObjRes:
                str_ciobj = str(ciObj)
                if str_ciobj != 'None':
                    df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(repo, ciObj, True, df, df6, lStagesProjectAdded)
        else:
            str_ciobj = str(ciObjRes)
            if str_ciobj != 'None':
                df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(repo, ciObjRes, True, df, df6, lStagesProjectAdded)

        return True,df,df3,df6,lStagesProjectAdded
    except:
        if len(literals)>0:
            found,df,df3,df6,lStagesProjectAdded = searchLiteralPathFromRoot_REC(repo, CITool, literals, df, df2,df3,df6,lStagesProjectAdded)
            return found,df,df3,df6,lStagesProjectAdded
        else:
            return False,df,df3,df6,lStagesProjectAdded

def searchLiteralPathFromRoot(repo, CITool, df, df2, df3, df6):
    aux.printLog("Buscando '" + CITool.value + "' en '" + repo.full_name + "'", logging.INFO)
    lStagesProjectAdded = [] # Lista de 'stages' a los que se les ha hecho un +1 en proyectos que lo utilizan.
    literals = ci.getCISearchFiles(CITool.value)
    for path in literals:
        encontrado = False
        try:
            c = getContents(repo, path)
            encontrado = True
        except:
            encontrado = False
        
        if encontrado:
            if not d.existsDFRecord(repo.full_name, df):
                df = d.addDFRecord(repo, df, True)
            
            df = d.updateDataFrameCiColumn(repo, "***", CITool, True, df)
            df2 = d.add1CounterDFRecord(CITool.value.lower(), "Encontrados_GitHub", df2)

            language = "None"
            if len(str(repo.language)) > 0:
                language = str(repo.language)
            if not d.existsDFRecord(language, df3):
                df3 = d.addLanguageDFRecord(language, df3)
            
            df3 = d.add1CounterDFRecord(language.lower(), CITool.value, df3)

            ciObjRes = ymlp.getParseObj(repo, path, CITool, True)
            if isinstance(ciObjRes, list):
                for ciObj in ciObjRes:
                    str_ciobj = str(ciObj)
                    if str_ciobj != 'None':
                        df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(repo, ciObj, True, df, df6, lStagesProjectAdded)
            else:
                str_ciobj = str(ciObjRes)
                if str_ciobj != 'None':
                    df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(repo, ciObjRes, True, df, df6, lStagesProjectAdded)

            return True,df,df3,df6
    
    return False,df,df3,df6

def searchInRepo(repo, literal):
    found = False
    contents = getContents(repo, "")
    while contents:
        contentFile = contents.pop(0)
        if literal in contentFile.path.lower():
            found = True
            break
        else:
            if contentFile.type == "dir":
                contents.extend(repo.get_contents(contentFile.path))
    return found

def searchInRoot(repo, literal):
    found = False
    contents = getContents(repo, "")
    for contentFile in contents:
        if literal in contentFile.path.lower():
            found = True
            break
    return found

def getAllRepoLanguages(languages_url):
    languages = []
    try:
        languages_response = requests.get(languages_url)
        text = languages_response.text
        loaded_json = json.loads(text)
        for l in loaded_json:
            languages.append(l)
    except:
        languages = []
    
    return languages