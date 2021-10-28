#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
from github import Github
import random
import auxiliares as aux
import datos as d
import busqueda as b

print("Iniciando proceso...")

try:
    # Generamos un token para consultar la API de GitHub a través de la librería.
    user = "jorcontrerasp"
    token = aux.leerFichero("token")
    g = Github(user, token)

    query = """
        language:java 
        stars:>=500 
        forks:>=300 
        created:<2015-01-01 
        pushed:>2020-01-01 
        archived:false 
        is:public 
    """

    q = aux.leerQuery("querys/query1")

    generator = g.search_repositories(query=q)

    # Convertimos el generador en una lista de repositorios.
    repositories = list(generator)

    # Guardamos la información de los repositorios recuperados en un archivo binario de Python.
    fRepos = "repos.pickle"
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
    randomizar = False
    lFinal = []
    if randomizar:
        while len(lFinal) < 500:
            item = random.choice(filteredRepos)
            if item not in lFinal:
                lFinal.append(item)
    else:
        lFinal = filteredRepos

    # Imprimimos la lista de repositorios
    aux.imprimirListaRepositorios(lFinal)

    # Generamos un DataFrame donde irán los resultados.
    df = d.generarDataFrame(lFinal)

    # Aplicamos el proceso.
    listaEncontrados = []
    listaEncontrados = b.busquedaGitHubApiRepos(filteredRepos, df)

    # Generamos un fichero EXCEL con los resultados.
    d.generarEXCEL(df, "resultados")

    print("Proceso finalizado.")

except:
    print("Se ha producido un ERROR inesperado.")
    raise
    # FIN