#Importamos las librerías necesarias.
import gitlab
import auxiliares as aux
import gitlab_search as gls
import datos as d

token = aux.leerFichero("gitlab_token")
gl = gitlab.Gitlab('http://gitlab.com', private_token=token)

project_id = 7764
project = gl.projects.get(project_id)

project_name_with_namespace = "gitlab-com/www-gitlab-com"
project2 = gl.projects.get(project_name_with_namespace)

lProjects = [project2]

identificador = project.attributes['path_with_namespace']
url = project.attributes['web_url']
languages = project.languages()

#path= '.gitlab/merge_request_templates/job-family-template.md'
#encontrado = gls.buscaRutaGitlab(project, path)
#print("Proyecto '" + identificador + "' encontrado: " + str(encontrado))

df = d.generarDataFrame(lProjects, False)
df2 = d.generarDataFrameContadores()

lEncontrados = gls.busquedaGitLabApiRepos(lProjects, df, df2)

d.generarEXCEL(df, "fExcelPruebas")
d.generarEXCEL(df2, "fExcelPruebas2")

print(str(len(lEncontrados)))

print("Fin de la prueba.")