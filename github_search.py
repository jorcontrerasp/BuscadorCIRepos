#Importamos las librerías necesarias.
from github import Github
import random
import auxiliares as aux
import herramientasCI as ci
import datos as d
import logging

def getGithubRepos():
    # Generamos un github_token para consultar la API de GitHub a través de la librería.
    user = "jorcontrerasp"
    token = aux.readFile("tokens/github_token.txt")
    g = Github(user, token)

    q = aux.readFile("github_querys/query2.txt")
    #query = mq.mGithubQuery.getQueryIni()
    generator = g.search_repositories(query=q)

    # Convertimos el generador en una lista de repositorios.
    repositories = list(generator)

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "github_repos.pickle"
    aux.makePickle(fRepos, repositories)
    repositories = aux.loadRepositories(fRepos)

    # Filtramos por el número de COMMITS.
    filterCommits = False

    MAX_COMMITS = 10000
    MIN_COMMITS = 1000
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
    randomizeRepos = True
    lFinal = []
    if randomizeRepos:
        while len(lFinal) < 10:
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
        found1 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI1, [], df, df2)
        found2 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI2, [], df, df2)
        found3 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI3, [], df, df2)
        found4 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI4, [], df, df2)
        found5 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI5, [], df, df2)
        found6 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI6, [], df, df2)
        found7 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI7, [], df, df2)
        found8 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI8, [], df, df2)
        found9 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI9, [], df, df2)
        found10 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI10, [], df, df2)
        found11 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI11, [], df, df2)
        found12 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI12, [], df, df2)
        found13 = searchLiteralPathFromRoot(repo, ci.HerramientasCI.CI13, [], df, df2)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                     or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(repo)

    d.updateTotalCounterDataFrame("Encontrados_GitHub", df, df2)

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
        d.updateDataFrame(repo, path, CITool, True, df)
        d.updateCounterDataFrame(CITool.value, "Encontrados_GitHub", df2)
        return True
    except:
        if len(literals)>0:
            return searchLiteralPathFromRoot(repo, CITool, literals, df, df2)
        else:
            return False

def searchLiteralPathFromRoot2(repo, path):
    try:
        repo.get_contents(path)
        return True
    except:
        return False

def searchLiteralPathFromRoot3(repo, contents, literal):
    found = False
    pLiteral = literal.split("/")
    cLiteral = pLiteral.pop(0)
    for contentFile in contents:
        itFile = aux.getItFile(contentFile.path)
        if cLiteral == itFile.lower():
            if len(pLiteral) > 0:
                if contentFile.type == "dir":
                    contents = repo.get_contents(contentFile.path)
                    found = searchLiteralPathFromRoot(repo, contents, '/'.join(pLiteral))
                    break
            else:
                found = True
    return found