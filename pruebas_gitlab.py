#Importamos las librerías necesarias.
import gitlab
import auxiliares as aux
import gitlab_search as gls
import datos as d

token = aux.readFile("tokens/gitlab_token.txt")
gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

project_id = 7764
project = gl.projects.get(project_id)

project_name_with_namespace = "gitlab-com/www-gitlab-com"
project2 = gl.projects.get(project_name_with_namespace)

lProjects = [project]

identificador = project.attributes['path_with_namespace']
url = project.attributes['web_url']
languages = project.languages()

#path= '.gitlab/merge_request_templates/job-family-template.md'
#encontrado = gls.buscaRutaGitlab(project, path)
#print("Proyecto '" + identificador + "' encontrado: " + str(encontrado))

df = d.makeDataFrame(lProjects, False)
df2 = d.makeCounterDataFrame()

lEncontrados = gls.searchProjectsGitLabApi(lProjects, df, df2)

d.makeEXCEL(df, "fExcelPruebas")
d.makeEXCEL(df2, "fExcelPruebas2")

print(str(len(lEncontrados)))

print("Fin de la prueba.")