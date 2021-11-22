#Importamos las librerías necesarias.
from github import Github
import random
import auxiliares as aux
import herramientasCI as ci
import datos as d
import montaGithubQuery as mq

def getRepositoriosGithub():
    # Generamos un github_token para consultar la API de GitHub a través de la librería.
    user = "jorcontrerasp"
    token = aux.leerFichero("github_token")
    g = Github(user, token)

    q = aux.leerQuery("github_querys/query2")
    #query = mq.mGithubQuery.getQueryIni()
    generator = g.search_repositories(query=q)

    # Convertimos el generador en una lista de repositorios.
    repositories = list(generator)

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "github_repos.pickle"
    aux.generarPickle(fRepos, repositories)
    repositories = aux.cargarRepositorios(fRepos)

    # Filtramos por el número de COMMITS.
    boFiltrarCommits = False

    MAX_COMMITS = 10000
    MIN_COMMITS = 1000
    filteredRepos = []

    if boFiltrarCommits:
        for repo in repositories:
            commits = repo.get_commits().totalCount
            if commits >= MIN_COMMITS and commits <= MAX_COMMITS:
                filteredRepos.append(repo)
    else:
        for repo in repositories:
            filteredRepos.append(repo)

    # Seleccionamos N repositorios de manera aleatoria:
    randomizar = True
    lFinal = []
    if randomizar:
        while len(lFinal) < 100:
            item = random.choice(filteredRepos)
            if item not in lFinal:
                lFinal.append(item)
    else:
        lFinal = filteredRepos

    # Imprimimos la lista de repositorios
    aux.imprimirListaRepositorios(lFinal)
    print("Nº de repositorios: " + str(len(lFinal)))

    return lFinal

def busquedaGitHubApiRepos(listaRepositorios, df, df2):
    listaEncontrados = []
    for repo in listaRepositorios:
        encontrado1 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI1, [], df, df2)
        encontrado2 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI2, [], df, df2)
        encontrado3 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI3, [], df, df2)
        encontrado4 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI4, [], df, df2)
        encontrado5 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI5, [], df, df2)
        encontrado6 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI6, [], df, df2)
        encontrado7 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI7, [], df, df2)
        encontrado8 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI8, [], df, df2)
        encontrado9 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI9, [], df, df2)
        encontrado10 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI10, [], df, df2)
        encontrado11 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI11, [], df, df2)
        encontrado12 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI12, [], df, df2)
        encontrado13 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI13, [], df, df2)

        # Si lo ha encontrado:
        # - lo añadimos a la listaEncontrados.
        encontrado = encontrado1 or encontrado2 or encontrado3 or encontrado4 or encontrado5 or encontrado6 or encontrado7 \
                     or encontrado8 or encontrado9 or encontrado10 or encontrado11 or encontrado12 or encontrado13
        if encontrado:
            listaEncontrados.append(repo)

    d.actualizarTotalesDataFrameContadores(df, df2)

    return listaEncontrados

def buscarEnRepo(repo, literal):
    encontrado = False
    contents = repo.get_contents("")
    while contents:
        content_file = contents.pop(0)
        if literal in content_file.path.lower():
            encontrado = True
            print(str(content_file.path))
            break
        else:
            if content_file.type == "dir":
                contents.extend(repo.get_contents(content_file.path))
    return encontrado

def buscarEnRaiz(repo, literal):
    encontrado = False
    contents = repo.get_contents("")
    for content_file in contents:
        if literal in content_file.path.lower():
            encontrado = True
            print(str(content_file.path))
            break
    return encontrado

def buscarRutaLiteralDesdeRaiz(repo, herramientaCI, literales, df, df2):
    print("Buscando '" + herramientaCI.value + "' en '" + repo.full_name + "'")
    try:
        if len(literales)==0:
            literales = ci.getFicherosBusquedaCI(herramientaCI.value)

        ruta = literales.pop(0)
        repo.get_contents(ruta)
        d.actualizarDataFrame(repo, ruta, herramientaCI, True, df)
        d.actualizarDataFrameContadores(herramientaCI.value, df2)
        return True
    except:
        if len(literales)>0:
            return buscarRutaLiteralDesdeRaiz(repo, herramientaCI, literales, df, df2)
        else:
            return False

def buscarRutaLiteralDesdeRaiz2(repo, ruta):
    try:
        repo.get_contents(ruta)
        return True
    except:
        return False

def buscarRutaLiteralDesdeRaiz3(repo, contents, literal):
    encontrado = False
    pLiteral = literal.split("/")
    cLiteral = pLiteral.pop(0)
    for contentFile in contents:
        ficheroIt = aux.obtenerFicheroIt(contentFile.path)
        if cLiteral == ficheroIt.lower():
            if len(pLiteral) > 0:
                if contentFile.type == "dir":
                    contents = repo.get_contents(contentFile.path)
                    encontrado = buscarRutaLiteralDesdeRaiz(repo, contents, '/'.join(pLiteral))
                    break
            else:
                encontrado = True
    return encontrado