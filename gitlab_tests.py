#AQUÍ irán las pruebas que se realicen sobre GitLab.

#Importamos las librerías necesarias.
import gitlab
import aux_functions as aux
import gitlab_search as gls
import dataF_functions as d

token = aux.readFile("tokens/gitlab_token.txt")
gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

project_name_with_namespace = "pycqa/flake8-docstrings"
project = gl.projects.get(project_name_with_namespace)

doTest = True

if doTest:
    
    lProjects = [project]

    df = d.makeDataFrame(lProjects, False)
    df2 = d.makeCounterDataFrame()
    df3 = d.makeEmptyLanguageDataFrame()
    df6 = d.makeEmptyStageStatisticsDataFrame()

    lEncontrados = gls.searchInProjectsGitLabApi(lProjects, df, df2, df3, df6)

    d.makeEXCEL(df2, "_counting")

print("Fin de la prueba.")