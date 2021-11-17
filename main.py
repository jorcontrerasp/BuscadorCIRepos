#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import datos as d
import github_search as ghs
import gitlab_search as gls

ejecutar = True
ejecutaProcesoGithub = False
ejecutaProcesoGitlab = True

def ejecutaProceso():
    try:
        print("Iniciando proceso...")

        if ejecutaProcesoGithub:
            # Obtenemos la lista de repositorios Github.
            lFinal = ghs.getRepositoriosGithub()

            # Generamos un DataFrame donde irán los resultados.
            githubDF = d.generarDataFrame(lFinal, True)

            # Generamos un DataFrame donde irán los contadores.
            githubDF2 = d.generarDataFrameContadores()

            # Aplicamos el proceso.
            listaEncontrados = []
            listaEncontrados = ghs.busquedaGitHubApiRepos(lFinal, githubDF, githubDF2)

            # Generamos un fichero EXCEL con los resultados.
            d.generarEXCEL(githubDF, "resultados_github")

            # Generamos un fichero EXCEL con los contadores.
            d.generarEXCEL(githubDF2, "contadores_github")

        if ejecutaProcesoGitlab:
            # Obtenemos la lista de repositorios Gitlab.
            lFinal = gls.getProyectosGitlab()

            # Generamos un DataFrame donde irán los resultados.
            gitlabDF = d.generarDataFrame(lFinal, False)

            # Generamos un DataFrame donde irán los contadores.
            gitlabDF2 = d.generarDataFrameContadores()

            # Aplicamos el proceso.
            listaEncontrados = []
            listaEncontrados = gls.busquedaGitLabApiRepos(lFinal, gitlabDF, gitlabDF2)

            # Generamos un fichero EXCEL con los resultados.
            d.generarEXCEL(gitlabDF, "resultados_gitlab")

            # Generamos un fichero EXCEL con los contadores.
            d.generarEXCEL(gitlabDF2, "contadores_gitlab")

        print("Proceso finalizado.")

    except:
        print("Se ha producido un ERROR inesperado.")
        raise
        # FIN

if ejecutar:
    ejecutaProceso()