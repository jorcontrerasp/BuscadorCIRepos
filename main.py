#TFG Grado en Ingeniería de Computadores

#Importamos las librerías necesarias.
import datos as d
import github_search as ghs
import gitlab_search as gls

ejecutar = True
ejecutaProcesoGithub = True
ejecutaProcesoGitlab = True

def ejecutaProceso():
    try:
        print("Iniciando proceso...")

        if ejecutaProcesoGithub:
            # Obtenemos la lista de repositorios Github.
            lFinal = ghs.getRepositoriosGithub()

            # Generamos un DataFrame donde irán los resultados.
            df = d.generarDataFrame(lFinal, True)

            # Aplicamos el proceso.
            listaEncontrados = []
            listaEncontrados = ghs.busquedaGitHubApiRepos(lFinal, df)

            # Generamos un fichero EXCEL con los resultados.
            d.generarEXCEL(df, "resultados_github")

        if ejecutaProcesoGitlab:
            # Obtenemos la lista de repositorios Gitlab.
            lFinal = gls.getProyectosGitlab()

            # Generamos un DataFrame donde irán los resultados.
            df2 = d.generarDataFrame(lFinal, False)

            # Aplicamos el proceso.
            listaEncontrados = []
            listaEncontrados = gls.busquedaGitLabApiRepos(lFinal, df2)

            # Generamos un fichero EXCEL con los resultados.
            d.generarEXCEL(df2, "resultados_gitlab")

        print("Proceso finalizado.")

    except:
        print("Se ha producido un ERROR inesperado.")
        raise
        # FIN

if ejecutar:
    ejecutaProceso()