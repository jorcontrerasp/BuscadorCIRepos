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

def getProyectosGitlab():
    # private github_token or personal github_token authentication
    token = aux.leerFichero("gitlab_token")
    gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

    i = 1
    lista = []
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

                    boVacio = esRepositorioVacio(project)
                    if not boVacio:
                        stars = project.star_count
                        if stars >= N_MIN_STARS:
                            if len(LANGUAGE)>0:
                                languages = project.languages()
                                for l in languages:
                                    if LANGUAGE.lower() == str(l).lower():
                                        lista.append(project)
                                        break
                            else:
                                lista.append(project)

                    tLista = len(lista)
                    aux.printLog("L Resultado: " + str(tLista), logging.INFO)
                    j = j + 1
                    if (tLista >= N_MAX_RESULT_PROYECTS):
                        break
                i = i + 1
                if (tLista >= N_MAX_RESULT_PROYECTS):
                    break
        except:
            aux.printLog(": Se ha producido un ERROR de búsqueda en la página " + str(i) + ".", logging.ERROR)
            i = i + 1

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.generarPickle(fRepos, lista)
    lista = aux.cargarRepositorios(fRepos)

    # Imprimimos la lista de proyectos
    aux.imprimirListaGitLabRepos(lista)
    aux.printLog("Nº de proyectos: " + str(len(lista)), logging.INFO)

    return lista

def busquedaGitLabApiRepos(listaProyectos, df, df2):
    listaEncontrados = []
    for proyecto in listaProyectos:
        encontrado1 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI1, df, df2)
        encontrado2 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI2, df, df2)
        encontrado3 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI3, df, df2)
        encontrado4 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI4, df, df2)
        encontrado5 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI5, df, df2)
        encontrado6 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI6, df, df2)
        encontrado7 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI7, df, df2)
        encontrado8 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI8, df, df2)
        encontrado9 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI9, df, df2)
        encontrado10 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI10, df, df2)
        encontrado11 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI11, df, df2)
        encontrado12 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI12, df, df2)
        encontrado13 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI12, df, df2)

        # Si lo ha encontrado:
        # - lo añadimos a la listaEncontrados.
        encontrado = encontrado1 or encontrado2 or encontrado3 or encontrado4 or encontrado5 or encontrado6 or encontrado7 \
                     or encontrado8 or encontrado9 or encontrado10 or encontrado11 or encontrado12 or encontrado13
        if encontrado:
            listaEncontrados.append(proyecto)

    d.actualizarTotalesDataFrameContadores(df, df2)

    return listaEncontrados

def buscaRutaGitlab(project, herramientaCI, df, df2):
    aux.printLog("Buscando '" + herramientaCI.value + "' en '" + project.attributes['path_with_namespace'] + "'", logging.INFO)
    encontrado = False
    try:
        paths = ci.getFicherosBusquedaCI(herramientaCI.value)
        for path in paths:
            items = project.repository_tree(all=True, path=path)
            if len(items) == 0:
                encontrado = existeFichero(project,path)
                if encontrado:
                    d.actualizarDataFrame(project, path, herramientaCI, False, df)
                    d.actualizarDataFrameContadores(herramientaCI.value, df2)
            else:
                encontrado = True
                d.actualizarDataFrame(project, path, herramientaCI, False, df)
                d.actualizarDataFrameContadores(herramientaCI.value, df2)
    except:
        d.actualizarDataFrame(project, "EXCEPT: ERROR al buscar la ruta en el proyecto", herramientaCI, False, df)
        aux.printLog("Se ha producido un ERROR al buscar la ruta en el proyecto GitLab.", logging.INFO)

def esRepositorioVacio(proyecto):
    return proyecto.attributes['empty_repo']

def esRepositorioVacio2(proyecto):
    try:
        items = proyecto.repository_tree()
        return False
    except:
        return True

def existeFichero(proyecto, fPath):
    try:
        f = proyecto.files.get(file_path=fPath, ref='master')
        return True
    except:
        return False