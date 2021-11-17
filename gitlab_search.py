#Importamos las librerías necesarias.
import gitlab
import auxiliares as aux
import herramientasCI as ci
import datos as d

N_MAX_PAGES = 12500
N_MIN_STARS = 50
N_MAX_RESULT_PROYECTS = 900
LANGUAGE = ''

def getProyectosGitlab():
    # private github_token or personal github_token authentication
    token = aux.leerFichero("gitlab_token")
    gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

    i = 1
    lista = []
    while i<=N_MAX_PAGES:
        try:
            projects = gl.projects.list(visibility='public',
                                        last_activity_after='2020-01-01T00:00:00Z',
                                        pagination='keyset',
                                        page=i,
                                        #per_page=100,
                                        order_by='id',
                                        sort='asc')

            print("Página " + str(i) + ": " + str(projects))
            print("Nº Proyectos: " + str(len(projects)))
            j = 0
            for project in projects:
                print("Tratando proyecto: " + str(j) + "/" + str(len(projects)))
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
                print("L Resultado: " + str(tLista))
                j = j + 1
                if (tLista >= N_MAX_RESULT_PROYECTS):
                    break
            i = i + 1
            if (tLista >= N_MAX_RESULT_PROYECTS):
                break
        except:
            print("Se ha producido un ERROR de búsqueda en la página " + str(i) + ".")
            i = i + 1

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "gitlab_repos.pickle"
    aux.generarPickle(fRepos, lista)
    lista = aux.cargarRepositorios(fRepos)

    return lista

def busquedaGitLabApiRepos(listaProyectos, df):
    listaEncontrados = []
    for proyecto in listaProyectos:
        encontrado0 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI0, df)
        encontrado1 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI1, df)
        encontrado2 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI2, df)
        encontrado3 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI3, df)
        encontrado4 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI4, df)
        encontrado5 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI5, df)
        encontrado6 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI6, df)
        encontrado7 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI7, df)
        encontrado8 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI8, df)
        encontrado9 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI9, df)
        encontrado10 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI10, df)
        encontrado11 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI11, df)
        encontrado12 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI12, df)
        encontrado13 = buscaRutaGitlab(proyecto, ci.HerramientasCI.CI12, df)

        # Si lo ha encontrado:
        # - lo añadimos a la listaEncontrados.
        encontrado = encontrado1 or encontrado2 or encontrado3 or encontrado4 or encontrado5 or encontrado6 or encontrado7 \
                     or encontrado8 or encontrado9 or encontrado10 or encontrado11 or encontrado12 or encontrado13
        if encontrado:
            listaEncontrados.append(proyecto)

    return listaEncontrados


def buscaRutaGitlab(project, herramientaCI, df):
    print("Buscando '" + herramientaCI.value + "' en '" + project.attributes['path_with_namespace'] + "'")
    encontrado = False
    try:
        paths = ci.getFicherosBusquedaCI(herramientaCI.value)
        for path in paths:
            items = project.repository_tree(all=True, path=path)
            if len(items) == 0:
                sPath = path.split("/")
                fichero = sPath.pop(len(sPath) - 1)
                path = "/".join(sPath)
                items = project.repository_tree(all=True, path=path)
                if len(items) == 0:
                    encontrado = False
                else:
                    for item in items:
                        iPath = item['path']
                        if iPath == (path + "/" + fichero):
                            encontrado = True
                            d.actualizarDataFrame(project, path + "/" + fichero, herramientaCI, False, df)
            else:
                encontrado = True
                d.actualizarDataFrame(project, path, herramientaCI, False, df)
    except:
        d.actualizarDataFrame(project, "EXCEPT: ERROR al buscar la ruta en el proyecto", herramientaCI, False, df)
        print("Se ha producido un ERROR al buscar la ruta en el proyecto GitLab.")

    return encontrado

def esRepositorioVacio(proyecto):
    try:
        items = proyecto.repository_tree()
        return False
    except:
        return True

def existeRutaFichero(proyecto, ruta):
    try:
        f = proyecto.files.get(file_path=ruta, ref='master')
        return True
    except:
        return False