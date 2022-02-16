#AQUÍ se implementará la búsqueda en GitLab.

#Importamos las librerías necesarias.
import gitlab
import aux_functions as aux
import dataF_functions as d
import ci_yml_parser as ymlp
import ci_tools as ci
import logging

# Configuración de la búsqueda GitLab.
config = "gitlab"
N_ERROR_PAGE_ATTEMPTS = ymlp.parseConfigParam(config, "N_ERROR_PAGE_ATTEMPTS")
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

def doSearchGitLabApi(df, df2, df3, df6):
    lFound = []
    lResult = []
    if search1By1:
        lFound,lResult = doSearch1By1GitLabApi(df, df2, df3, df6)
    else:
        # Obtenemos la lista de repositorios Gitlab.
        lFound = getGitLabProjects()

        # Aplicamos el proceso.
        lResult = searchInProjectsGitLabApi(lFound, df, df2, df3, df6)

    return lFound,lResult

def authenticate():
    # AUTHENTICATE
    token = aux.readFile("tokens/gitlab_token.txt")
    gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

    return gl

def listProyectsGitLabApi(idAfter):
    # AUTHENTICATE
    gl = authenticate()

    # GET PROJECTS
    projects = gl.projects.list(visibility='public', 
                                        last_activity_after='2016-01-01T00:00:00Z', 
                                        pagination='keyset', 
                                        id_after=idAfter, 
                                        page=1, 
                                        order_by='id', 
                                        sort='asc')
    return projects

def doSearch1By1GitLabApi(df, df2, df3, df6):
    errorAttempts = 0
    i = 1
    lFound = []
    lResult = []
    idAfter = 0
    while i<=N_MAX_SEARCHES:
        try:

            if errorAttempts >= N_ERROR_PAGE_ATTEMPTS:
                idAfter = idAfter + 20
                errorAttempts = 0
            
            projects = listProyectsGitLabApi(idAfter)

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
                                        found,df,df3,df6 = searchInProjectGitLabApi(project, df, df2, df3, df6)
                                        if found:
                                            lResult.append(project)
                                        break
                            else:
                                lFound.append(project)
                                found,df,df3,df6 = searchInProjectGitLabApi(project, df, df2, df3, df6)
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
        except Exception as e:
            aux.printLog(": Se ha producido un ERROR de búsqueda en la página " + str(i) + ".", logging.ERROR)
            aux.writeInLogFile("EXCEPT --> página: " + str(i) + "; idAfter: " + str(idAfter) + "; [" + str(e) + "]")
            errorAttempts = errorAttempts + 1
            i = i + 1
    
    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.makePickle(fRepos, lFound)
    lFound = aux.loadRepositories(fRepos)
    
    # Imprimimos la lista de proyectos
    aux.printLog("Nº de proyectos: " + str(len(lFound)), logging.INFO)

    df,df2,df4,df5 = d.doAuxWithResultsDF(df, df2, False)

    # Generamos un fichero EXCEL con los resultados.
    d.makeEXCEL(df, "gitlab_results")
    d.makeEXCEL(df3, "gitlab_languages")
    d.makeEXCEL(df4, "gitlab_language_statistics")
    d.makeEXCEL(df5, "gitlab_ci_statistics")
    d.makeEXCEL(df6, "gitlab_stage_statistics")
    
    return lFound,lResult

def getGitLabProjects():
    i = 1
    lResult = []
    idAfter = 0
    while i<=N_MAX_SEARCHES:
        try:

            if errorAttempts >= N_ERROR_PAGE_ATTEMPTS:
                idAfter = idAfter + 20
                errorAttempts = 0

            projects = listProyectsGitLabApi(idAfter)

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
            aux.writeInLogFile("EXCEPT --> página: " + str(i) + "; idAfter: " + str(idAfter) + "; [" + str(e) + "]")
            errorAttempts = errorAttempts + 1
            i = i + 1

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.makePickle(fRepos, lResult)
    lResult = aux.loadRepositories(fRepos)

    # Imprimimos la lista de proyectos
    aux.printGitLabProyectList(lResult)
    aux.printLog("Nº de proyectos: " + str(len(lResult)), logging.INFO)

    return lResult

def searchInProjectGitLabApi(project, df, df2, df3, df6):
    if not onlyPositives and not d.existsDFRecord(project.attributes['path_with_namespace'], df):
        df = d.addDFRecord(project, df, False)

    found1,df,df3,df6 = searchGitLabPath(project, ci.HerramientasCI.CI1, df, df2, df3, df6)
    found2,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI2, df, df2, df3, df6)
    found3,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI3, df, df2, df3, df6)
    found4,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI4, df, df2, df3, df6)
    found5,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI5, df, df2, df3, df6)
    found6,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI6, df, df2, df3, df6)
    found7,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI7, df, df2, df3, df6)
    found8,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI8, df, df2, df3, df6)
    found9,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI9, df, df2, df3, df6)
    found10,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI10, df, df2, df3, df6)
    found11,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI11, df, df2, df3, df6)
    found12,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3, df6)
    found13,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3, df6)

    # Si lo ha encontrado:
    found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                    or found8 or found9 or found10 or found11 or found12 or found13

    return found,df,df3,df6

def searchInProjectsGitLabApi(lProjects, df, df2, df3, df6):
    lFound = []
    for project in lProjects:
        if not onlyPositives and not d.existsDFRecord(project.attributes['path_with_namespace'], df):
            df = d.addDFRecord(project, df, False)

        found1,df,df3,df6 = searchGitLabPath(project, ci.HerramientasCI.CI1, df, df2, df3, df6)
        found2,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI2, df, df2, df3, df6)
        found3,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI3, df, df2, df3, df6)
        found4,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI4, df, df2, df3, df6)
        found5,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI5, df, df2, df3, df6)
        found6,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI6, df, df2, df3, df6)
        found7,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI7, df, df2, df3, df6)
        found8,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI8, df, df2, df3, df6)
        found9,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI9, df, df2, df3, df6)
        found10,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI10, df, df2, df3, df6)
        found11,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI11, df, df2, df3, df6)
        found12,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3, df6)
        found13,df,df3,df6  = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2, df3, df6)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                     or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(project)

    df,df2,df4,df5 = d.doAuxWithResultsDF(df, df2, False)

    # Generamos ficheros EXCEL con los resultados.
    d.makeEXCEL(df, "gitlab_results")
    d.makeEXCEL(df3, "gitlab_languages")
    d.makeEXCEL(df4, "gitlab_language_statistics")
    d.makeEXCEL(df5, "gitlab_ci_statistics")
    d.makeEXCEL(df6, "gitlab_stage_statistics")

    return lFound

def searchGitLabPath(project, CITool, df, df2, df3, df6):
    aux.printLog("Buscando '" + CITool.value + "' en '" + project.attributes['path_with_namespace'] + "'", logging.INFO)
    found = False
    try:
        paths = ci.getCISearchFiles(CITool.value)
        for path in paths:
            items = project.repository_tree(all=True, path=path)
            if len(items) == 0:
                found = isFile(project,path)
                if found:
                    if not d.existsDFRecord(project.attributes['path_with_namespace'], df):
                        df = d.addDFRecord(project, df, False)
                    
                    df = d.updateDataFrameCiColumn(project, "***", CITool, False, df)
                    df2 = d.add1CounterDFRecord(CITool.value, "Encontrados_GitLab", df2)

                    languages = project.languages()
                    language = getFirstBackendLanguage(languages)

                    if not d.existsDFRecord(language, df3):
                        df3 = d.addLanguageDFRecord(language, df3)
                    
                    df3 = d.add1CounterDFRecord(language, CITool.value, df3)

                    ciObjRes = ymlp.getParseObj(project, path, CITool, False)
                    lStagesProjectAdded = []
                    if isinstance(ciObjRes, list):
                        for ciObj in ciObjRes:
                            str_ciobj = str(ciObj)
                            if str_ciobj != 'None':
                                df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(project, ciObj, False, df, df6, lStagesProjectAdded)
                    else:
                        str_ciobj = str(ciObjRes)
                        if str_ciobj != 'None':
                            df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(project, ciObjRes, False, df, df6, lStagesProjectAdded)
                        
            else:
                found = True
                if not d.existsDFRecord(project.attributes['path_with_namespace'], df):
                    df = d.addDFRecord(project, df, False)
                
                df = d.updateDataFrameCiColumn(project, "***", CITool, False, df)
                df2 = d.add1CounterDFRecord(CITool.value, "Encontrados_GitLab", df2)

                languages = project.languages()
                language = getFirstBackendLanguage(languages)

                if not d.existsDFRecord(language, df3):
                    df3 = d.addLanguageDFRecord(language, df3)
                
                df3 = d.add1CounterDFRecord(language, CITool.value, df3)

                ciObjRes = ymlp.getParseObj(project, path, CITool, False)
                lStagesProjectAdded = []
                if isinstance(ciObjRes, list):
                    for ciObj in ciObjRes:
                        str_ciobj = str(ciObj)
                        if str_ciobj != 'None':
                            df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(project, ciObj, False, df, df6, lStagesProjectAdded)
                else:
                    str_ciobj = str(ciObjRes)
                    if str_ciobj != 'None':
                        df,df6,lStagesProjectAdded = d.updateDataFrameCiObj(project, ciObjRes, False, df, df6, lStagesProjectAdded)
    except:
        aux.printLog("Se ha producido un ERROR al buscar la ruta en el proyecto GitLab.", logging.INFO)

    return found,df,df3,df6

def getFrontendLanguages():
    frontLanguages = []
    frontLanguages.append("html")
    frontLanguages.append("css")
    frontLanguages.append("scss")
    frontLanguages.append("haml")
    return frontLanguages

def getBackendLanguages(languages):
    frontLanguages = getFrontendLanguages()
    backendLanguages = []
    if len(languages)>0:
        for l in languages:
            blockLanguage = False
            for frontL in frontLanguages:
                if l.lower() == frontL.lower():
                    blockLanguage = True
                    break
            if not blockLanguage:
                backendLanguages.append(l)
    return backendLanguages

def getFirstBackendLanguage(languages):
    frontLanguages = getFrontendLanguages()
    language = "None"
    if len(languages)>0:
        for l in languages:
            blockLanguage = False
            for frontL in frontLanguages:
                if l.lower() == frontL.lower():
                    blockLanguage = True
                    break
            if not blockLanguage:
                language = l
                break
    return language

def isEmptyProject(project):
    return project.attributes['empty_repo']

def isEmptyProject2(project):
    try:
        items = project.repository_tree()
        return False
    except:
        return True

def isFile(project, fPath):
    try:
        f = project.files.get(file_path=fPath, ref='master')
        return True
    except:
        return False