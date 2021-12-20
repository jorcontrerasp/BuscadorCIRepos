#AQUÍ se implementará la búsqueda en GitHub.

#Importamos las librerías necesarias.
from github import Github
import random
import aux_functions as aux
import ci_tools as ci
import dataF_functions as d
import logging
import yaml_parser as ymlp

# Configuración de la búsqueda GitHub.
config = "github"
queryFile = ymlp.parseConfigParam(config, "queryFile")
filterCommits = ymlp.parseConfigParam(config, "filterCommits")
MAX_COMMITS = ymlp.parseConfigParam(config, "MAX_COMMITS")
MIN_COMMITS = ymlp.parseConfigParam(config, "MIN_COMMITS")
randomizeRepos = ymlp.parseConfigParam(config, "randomizeRepos")
N_RANDOM = ymlp.parseConfigParam(config, "N_RANDOM")
onlyPositives = ymlp.parseConfigParam(config, "onlyPositives")

def getGithubRepos():
    # Generamos un github_token para consultar la API de GitHub a través de la librería.
    user = "jorcontrerasp"
    token = aux.readFile("tokens/github_token.txt")
    g = Github(user, token)

    q = aux.readFile(queryFile)
    #query = mq.mGithubQuery.getQueryIni()
    aux.printLog("Ejecutando query: " + queryFile, logging.INFO)
    generator = g.search_repositories(query=q)

    # Convertimos el generador en una lista de repositorios.
    aux.printLog("Generando lista de repositorios GitHub...", logging.INFO)
    repositories = list(generator)

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "github_repos.pickle"
    aux.makePickle(fRepos, repositories)
    repositories = aux.loadRepositories(fRepos)

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

    # Imprimimos la lista de repositorios
    aux.printGitHubRepoList(lFinal)
    aux.printLog("Nº de repositorios: " + str(len(lFinal)), logging.INFO)

    return lFinal

def searchReposGitHubApi(lRepositories, df, df2):
    lFound = []
    for repo in lRepositories:

        if not onlyPositives and not d.existsDFRecord(repo.full_name, df):
            df = d.addDFRecord(repo, df, True)


        found1,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI1, df, df2)
        found2,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI2, df, df2)
        found3,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI3, df, df2)
        found4,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI4, df, df2)
        found5,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI5, df, df2)
        found6,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI6, df, df2)
        found7,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI7, df, df2)
        found8,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI8, df, df2)
        found9,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI9, df, df2)
        found10,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI10, df, df2)
        found11,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI11, df, df2)
        found12,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI12, df, df2)
        found13,df = searchLiteralPathFromRoot2(repo, ci.HerramientasCI.CI13, df, df2)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                     or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(repo)

    df2 =d.updateTotalCounterDataFrame("Encontrados_GitHub", df, df2)

    # Generamos un fichero EXCEL con los resultados.
    d.makeEXCEL(df, "resultados_github")

    return lFound

def searchInRepo(repo, literal):
    found = False
    contents = repo.get_contents("")
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
    contents = repo.get_contents("")
    for contentFile in contents:
        if literal in contentFile.path.lower():
            found = True
            break
    return found

def searchLiteralPathFromRoot(repo, CITool, literals, df, df2):
    aux.printLog("Buscando '" + CITool.value + "' en '" + repo.full_name + "'", logging.INFO)
    try:
        if len(literals)==0:
            literals = ci.getCISearchFiles(CITool.value)

        path = literals.pop(0)
        repo.get_contents(path)

        if d.existsDFRecord(repo.full_name, df):
            df = d.updateDataFrame(repo, "***", CITool, True, df)
            if not onlyPositives:
                df2 = d.updateCounterDataFrame(CITool.value, "Encontrados_GitHub", df2)
        else:
            df = d.addDFRecord(repo, df, True)
            df = d.updateDataFrame(repo, "***", CITool, True, df)
            df2 = d.updateCounterDataFrame(CITool.value, "Encontrados_GitHub", df2)

        return True,df
    except:
        if len(literals)>0:
            found,df = searchLiteralPathFromRoot(repo, CITool, literals, df, df2)
            return found,df
        else:
            return False,df

def searchLiteralPathFromRoot2(repo, CITool, df, df2):
    aux.printLog("Buscando '" + CITool.value + "' en '" + repo.full_name + "'", logging.INFO)
    literals = ci.getCISearchFiles(CITool.value)

    for path in literals:
        encontrado = False
        try:
            c = repo.get_contents(path)
            encontrado = True
        except:
            encontrado = False
        
        if encontrado:
            if not d.existsDFRecord(repo.full_name, df):
                df = d.addDFRecord(repo, df, True)
            
            df = d.updateDataFrame(repo, "***", CITool, True, df)
            df2 = d.updateCounterDataFrame(CITool.value, "Encontrados_GitHub", df2)

            return True,df
    
    return False,df