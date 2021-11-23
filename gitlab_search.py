#Importamos las librerías necesarias.
import gitlab
import auxiliares as aux
import herramientasCI as ci
import datos as d
import logging

N_MAX_SEARCHES = 18550
N_MIN_STARS = 50
N_MAX_RESULT_PROYECTS = 10
LANGUAGE = ''

def getGitlabProyects():
    # private github_token or personal github_token authentication
    token = aux.readFile("gitlab_token.txt")
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
                            if len(LANGUAGE)>0:
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
                    if (lResultSize >= N_MAX_RESULT_PROYECTS):
                        break
                i = i + 1
                if (lResultSize >= N_MAX_RESULT_PROYECTS):
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

def searchProyectsGitLabApi(lProjects, df, df2):
    lFound = []
    for project in lProjects:
        found1 = searchGitLabPath(project, ci.HerramientasCI.CI1, df, df2)
        found2 = searchGitLabPath(project, ci.HerramientasCI.CI2, df, df2)
        found3 = searchGitLabPath(project, ci.HerramientasCI.CI3, df, df2)
        found4 = searchGitLabPath(project, ci.HerramientasCI.CI4, df, df2)
        found5 = searchGitLabPath(project, ci.HerramientasCI.CI5, df, df2)
        found6 = searchGitLabPath(project, ci.HerramientasCI.CI6, df, df2)
        found7 = searchGitLabPath(project, ci.HerramientasCI.CI7, df, df2)
        found8 = searchGitLabPath(project, ci.HerramientasCI.CI8, df, df2)
        found9 = searchGitLabPath(project, ci.HerramientasCI.CI9, df, df2)
        found10 = searchGitLabPath(project, ci.HerramientasCI.CI10, df, df2)
        found11 = searchGitLabPath(project, ci.HerramientasCI.CI11, df, df2)
        found12 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2)
        found13 = searchGitLabPath(project, ci.HerramientasCI.CI12, df, df2)

        # Si lo ha encontrado:
        # - lo añadimos a la lista de encontrados.
        found = found1 or found2 or found3 or found4 or found5 or found6 or found7 \
                     or found8 or found9 or found10 or found11 or found12 or found13
        if found:
            lFound.append(project)

    d.updateTotalCounterDataFrame(df, df2)

    return lFound

def searchGitLabPath(project, CITool, df, df2):
    aux.printLog("Buscando '" + CITool.value + "' en '" + project.attributes['path_with_namespace'] + "'", logging.INFO)
    found = False
    try:
        paths = ci.getCISearchFiles(CITool.value)
        for path in paths:
            items = project.repository_tree(all=True, path=path)
            if len(items) == 0:
                found = existsFile(project,path)
                if found:
                    d.updateDataFrame(project, path, CITool, False, df)
                    d.updateCounterDataFrame(CITool.value, df2)
            else:
                found = True
                d.updateDataFrame(project, path, CITool, False, df)
                d.updateCounterDataFrame(CITool.value, df2)
    except:
        d.updateDataFrame(project, "EXCEPT: ERROR al buscar la ruta en el proyecto", CITool, False, df)
        aux.printLog("Se ha producido un ERROR al buscar la ruta en el proyecto GitLab.", logging.INFO)

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