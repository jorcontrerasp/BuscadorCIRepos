#AQUÍ irán las pruebas que se realicen sobre GitLab.

#Importamos las librerías necesarias.
import gitlab
import aux_functions as aux
import gitlab_search as gls
import dataF_functions as d

token = aux.readFile("tokens/gitlab_token.txt")
gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

#project_id = 7764
#project = gl.projects.get(project_id)

#project_name_with_namespace = "gitlab-com/www-gitlab-com"
#project2 = gl.projects.get(project_name_with_namespace)

project_name_with_namespace = "gitlab-examples/ssh-private-key"
project = gl.projects.get(project_name_with_namespace)

lProjects = [project]

identificador = project.attributes['path_with_namespace']
url = project.attributes['web_url']
languages = project.languages()

#path= '.gitlab/merge_request_templates/job-family-template.md'
#encontrado = gls.buscaRutaGitlab(project, path)
#print("Proyecto '" + identificador + "' encontrado: " + str(encontrado))

df = d.makeDataFrame(lProjects, False)
df2 = d.makeCounterDataFrame()
df3 = d.makeEmptyLanguageDataFrame()

lEncontrados = gls.searchInProjectsGitLabApi(lProjects, df, df2, df3)

d.makeEXCEL(df2, "_contadores")

print("Fin de la prueba.")