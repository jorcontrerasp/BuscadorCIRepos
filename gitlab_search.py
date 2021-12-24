#AQUÍ se implementará la búsqueda en GitLab.

#Importamos las librerías necesarias.
import gitlab
import aux_functions as aux
import ci_tools as ci
import dataF_functions as d
import logging
import yaml_parser as ymlp

# Configuración de la búsqueda GitLab.
config = "gitlab"
LANGUAGE = ymlp.parseConfigParam(config, "LANGUAGE")
N_MAX_SEARCHES = ymlp.parseConfigParam(config, "N_MAX_SEARCHES")
N_MIN_STARS = ymlp.parseConfigParam(config, "N_MIN_STARS")
onlyPositives = ymlp.parseConfigParam(config, "onlyPositives")
N_MAX_PROJECTS = ymlp.parseConfigParam(config, "N_MAX_PROJECTS")
# Para GitLab, si solo queremos positivos, da igual lo que venga en search1By1. Hay que buscar 1 por 1 sí o sí.
if onlyPositives:
    search1By1 = True
else:
    search1By1 = ymlp.parseConfigParam(config, "search1By1")

def doSearchGitLabApi(df, df2, df3):
    lFound = []
    lResult = []
    if search1By1:
        lFound,lResult = doSearch1By1GitLabApi(df, df2, df3)
    else:
        # Obtenemos la lista de repositorios Gitlab.
        lFound = getGitlabProjects()

        # Aplicamos el proceso.
        lResult = searchInProjectsGitLabApi(lFound, df, df2, df3)

    return lFound,lResult

def doSearch1By1GitLabApi(df, df2, df3):
    # private github_token or personal github_token authentication
    token = aux.readFile("tokens/gitlab_token.txt")
    gl = gitlab.Gitlab('http://gitlab.com', private_token=token)
    
    i = 1
    lFound = []
    lResult = []
    idAfter = 0
    while i<=N_MAX_SEARCHES:
        try:
            projects = gl.projects.list(visibility='public',
                                        ast_activity_after='2020-01-01T00:00:00Z',
                                        #all=True,
                                        pagination='keyset',
                                        id_after=idAfter,
                                        #use_keyset_pagination=True,
                                        page=1,
                                        #per_page=100,
                                        order_by='id',
                                        sort='asc'
                                        )
            if len(projects)==0:
                aux.printLog("No se ha encontrado ningún projecto en la búsqueda " + str(i), logging.WARNING)
                break
            else:
                aux.printLog("Búsqueda " + str(i), logging.INFO)
                aux.printLog("Nº Proyectos: " + str(len(projects)), logging.INFO)
                j = 1
                for project in projects:
                    aux.printLog("Tratando proyecto: " + str(j) + "/" + str(len(projects)), logging.INFO)
                    
                    if(j==len(projects)):
                        idAfter = project.attributes['id']
                        
                    empty = isEmptyProject(project)
                    if not empty:
                        stars = project.star_count
                        if stars >= N_MIN_STARS:
                            if LANGUAGE != "ALL":
                                languages = project.languages()
                                for l in languages:
                                    if LANGUAGE.lower() == str(l).lower():
                                        lFound.append(project)
                                        found,df,df3 = searchInProjectGitLabApi(project, df, df2, df3)
                                        if found:
                                            lResult.append(project)
                                        break
                            else:
                                lFound.append(project)
                                found,df,df3 = searchInProjectGitLabApi(project, df, df2, df3)
                                if found:
                                    lResult.append(project)

                    # Si solo buscamos positivos la condición de parada es cuando tengamos N_MAX_POSITIVES sobre la lista de positivos.
                    # # Si buscamos no solo positivos, la condición de parada será N_MAX_RESULT_PROYECTS sobre la lista resultado.
                    if onlyPositives:
                        lSize = len(lResult)
                    else:
                        lSize = len(lFound)
                        
                    aux.printLog("Lista tratados: " + str(len(lFound)), logging.INFO)
                    aux.printLog("Lista positivos: " + str(len(lResult)), logging.INFO)
                    j = j + 1
                    if (lSize >= N_MAX_PROJECTS):
                        break
                i = i + 1
                if (lSize >= N_MAX_PROJECTS):
                    break
        except:
            aux.printLog(": Se ha producido un ERROR de búsqueda en la página " + str(i) + ".", logging.ERROR)
            i = i + 1
    
    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.makePickle(fRepos, lFound)
    lFound = aux.loadRepositories(fRepos)
    
    # Imprimimos la lista de proyectos
    aux.printLog("Nº de proyectos: " + str(len(lFound)), logging.INFO)

    df2 = d.updateTotalCounterDataFrame("Encontrados_GitLab", df, df2)

    # Generamos un fichero EXCEL con los resultados.
    d.makeEXCEL(df, "resultados_gitlab")
    d.makeEXCEL(df3, "lenguajes_gitlab")
    
    return lFound,lResult

def getGitlabProjects():
    # private github_token or personal github_token authentication
    token = aux.readFile("tokens/gitlab_token.txt")
    gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

    i = 1
    lResult = []
    idAfter = 0
    while i<=N_MAX_SEARCHES:
        try:

            projects = gl.projects.list(visibility='public',
                                        last_activity_after='2020-01-01T00:00:00Z',
                                        #all=True,
                                        pagination='keyset',
                                        id_after=idAfter,
                                        #use_keyset_pagination=True,
                                        page=1,
                                        #per_page=100,
                                        order_by='id',
                                        sort='asc'
                                        )

            if len(projects)==0:
                aux.printLog("No se ha encontrado ningún projecto en la búsqueda " + str(i), logging.WARNING)
                break
            else:
                aux.printLog("Búsqueda " + str(i), logging.INFO)
                aux.printLog("Nº Proyectos: " + str(len(projects)), logging.INFO)
                j = 1
                for project in projects:
                    aux.printLog("Tratando proyecto: " + str(j) + "/" + str(len(projects)), logging.INFO)

                    if(j==len(projects)):
                        idAfter = project.attributes['id']

                    empty = isEmptyProject(project)
                    if not empty:
                        stars = project.star_count
                        if stars >= N_MIN_STARS:
                            if LANGUAGE != "ALL":
                                languages = project.languages()
                                for l in languages:
                                    if LANGUAGE.lower() == str(l).lower():
                                        lResult.append(project)
                                        break
                            else:
                                lResult.append(project)

                    lResultSize = len(lResult)
                    aux.printLog("L Resultado: " + str(lResultSize), logging.INFO)
                    j = j + 1
                    if (lResultSize >= N_MAX_PROJECTS):
                        break
                i = i + 1
                if (lResultSize >= N_MAX_PROJECTS):
                    break
        except:
            aux.printLog(": Se ha producido un ERROR de búsqueda en la página " + str(i) + ".", logging.ERROR)
            i = i + 1

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.makePickle(fRepos, lResult)
    lResult = aux.loadRepositories(fRepos)

    # Imprimimos la lista de proyectos
    aux.printGitLabProyectList(lResult)
    aux.printLog("Nº de proyectos: " + str(len(lResult)), logging.INFO)

    return lResult

def searchInProjectGitLabApi(project, df, df2, df3):
    if not onlyPositives and not d.existsDFRecord(project.attributes['path_with_namespace'], df):
        df = d.addDFRecord(project, df, False)

    found1,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI1, df, df2, df3)
    found2,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI2, df, df2, df3)
    found3,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI3, df, df2, df3)
    found4,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI4, df, df2, df3)
    found5,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI5, df, df2, df3)
    found6,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI6, df, df2, df3)
    found7,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI7, df, df2, df3)
    found8,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI8, df, df2, df3)
    found9,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI9, df, df2, df3)
    found10,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI10, df, df2, df3)
    found11,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI11, df, df2, df3)
    found12,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3)
    found13,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3)

    # Si lo ha encontrado:
    # - lo añadimos a la lista de encontrados.
    found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                    or found8 or found9 or found10 or found11 or found12 or found13

    return found,df,df3

def searchInProjectsGitLabApi(lProjects, df, df2, df3):
    lFound = []
    for project in lProjects:
        if not onlyPositives and not d.existsDFRecord(project.attributes['path_with_namespace'], df):
            df = d.addDFRecord(project, df, False)

        found1,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI1, df, df2, df3)
        found2,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI2, df, df2, df3)
        found3,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI3, df, df2, df3)
        found4,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI4, df, df2, df3)
        found5,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI5, df, df2, df3)
        found6,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI6, df, df2, df3)
        found7,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI7, df, df2, df3)
        found8,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI8, df, df2, df3)
        found9,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI9, df, df2, df3)
        found10,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI10, df, df2, df3)
        found11,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI11, df, df2, df3)
        found12,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3)
        found13,df,df3 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                     or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(project)

    df2 = d.updateTotalCounterDataFrame("Encontrados_GitLab", df, df2)

    # Generamos ficheros EXCEL con los resultados.
    d.makeEXCEL(df, "resultados_gitlab")
    d.makeEXCEL(df3, "lenguajes_gitlab")

    return lFound

def searchGitLabPath(project, CITool, df, df2, df3):
    aux.printLog("Buscando '" + CITool.value + "' en '" + project.attributes['path_with_namespace'] + "'", logging.INFO)
    found = False
    try:
        paths = ci.getCISearchFiles(CITool.value)
        for path in paths:
            items = project.repository_tree(all=True, path=path)
            if len(items) == 0:
                found = existsFile(project,path)
                if found:
                    if not d.existsDFRecord(project.attributes['path_with_namespace'], df):
                        df = d.addDFRecord(project, df, False)
                    
                    df = d.updateDataFrame(project, "***", CITool, False, df)
                    df2 = d.add1CounterDFRecord(CITool.value, "Encontrados_GitLab", df2)

                    language = "None"
                    languages = project.languages()
                    if len(languages)>0:
                        for l in languages:
                            language = l
                            break

                    if not d.existsDFRecord(language, df3):
                        df3 = d.addLanguageDFRecord(language, df3)
                    
                    df3 = d.add1CounterDFRecord(language, CITool.value, df3)

                    ciObj = ymlp.getParseObj(repo, path, CITool, False)
                    if not type(ciObj) == None:
                        print("ciObj NOT NULL")
                    else:
                        print("ciObj NULL")
                        
            else:
                found = True
                if not d.existsDFRecord(project.attributes['path_with_namespace'], df):
                        df = d.addDFRecord(project, df, False)
                
                df = d.updateDataFrame(project, "***", CITool, False, df)
                df2 = d.add1CounterDFRecord(CITool.value, "Encontrados_GitLab", df2)

                language = "None"
                languages = project.languages()
                if len(languages)>0:
                    for l in languages:
                        language = l
                        break

                if not d.existsDFRecord(language, df3):
                    df3 = d.addLanguageDFRecord(language, df3)
                
                df3 = d.add1CounterDFRecord(language, CITool.value, df3)

                ciObj = ymlp.getParseObj(repo, path, CITool, False)
                if not type(ciObj) == None:
                    print("ciObj NOT NULL")
                else:
                    print("ciObj NULL")
    except:
        aux.printLog("Se ha producido un ERROR al buscar la ruta en el proyecto GitLab.", logging.INFO)

    return found,df,df3

def isEmptyProject(project):
    return project.attributes['empty_repo']

def isEmptyProject2(project):
    try:
        items = project.repository_tree()
        return False
    except:
        return True

def existsFile(project, fPath):
    try:
        f = project.files.get(file_path=fPath, ref='master')
        return True
    except:
        return False