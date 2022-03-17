#AQUÍ irán las pruebas que se realicen sobre GitLab.

#Importamos las librerías necesarias.
import gitlab
import aux_functions as aux
import gitlab_search as gls
import dataF_functions as d

token = aux.readFile("tokens/gitlab_token.txt")
gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

# gitlab-com/www-gitlab-com
# gitlab-org/gitlab-foss
# pycqa/flake8-docstrings
# gitlab-data/analytics --> ¿emoticonos a los stages?
# zaaksysteem/zaaksysteem --> Se está haciendo lower() de los STAGES, ¿es lo mismo release que Release, por ejemplo? 
# Millennium_Dawn/Millennium_Dawn
# xonotic/xonotic-data.pk3dir
# timvisee/ffsend
# mailman/mailman
project_name_with_namespace = "gitlab-com/www-gitlab-com"
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