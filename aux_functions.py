#AQUÍ se definirán las funciones auxiliares del programa.

#Importamos las librerías necesarias.
import pickle
import datetime
import logging
import base64
from github import GithubException
import ci_yml_parser as ymlp
import gitlab_search as gls
import github_search as ghs

def makePickle(fileName, lRepositories):
    printLog("Generando fichero pickle...", logging.INFO)
    with open(fileName, 'wb') as f:
        pickle.dump(lRepositories, f)
    printLog("Fichero " + fileName + " generado", logging.INFO)

def loadRepositories(file):
    printLog("Cargando repositorios...", logging.INFO)
    with open(file, 'rb') as f:
        repositories = pickle.load(f)
    return repositories

def printGitHubRepoList(repositories):
    print("Lista de repositorios: ")
    for project in repositories:
        projectName = project.full_name.split("/")[1]
        print(project.full_name)

def printGitLabProyectList(projects):
    print("Lista de proyectos: ")
    for project in projects:
        print(project.attributes['path_with_namespace'])

def getItFile(path):
    if "/" in path:
        pathArray = path.split("/")
        fIt = pathArray[len(pathArray) - 1]
    else:
        fIt = path
    return fIt

def readFile(file):
    with open(file, 'rb') as f:
        content = f.read()
        r = str(content.decode())
        f.close()
        return r

def printLog(msg, level):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s'
                  , datefmt='%d/%m/%y %H:%M:%S'
                  , level=logging.INFO)

    if level == logging.INFO:
        logging.info(msg)
    elif level == logging.WARNING:
        logging.warning(msg)
    elif level == logging.ERROR:
        logging.error(msg)
    elif level == logging.CRITICAL:
        logging.critical(msg)
    else:
        logging.info(msg)

def getTimestamp():
    timestamp = str(datetime.datetime.now())[0:19]
    return timestamp

def getBlobContent(project, branch, path_name):
    # Obtener referencia del "branch"
    ref = project.get_git_ref(f'heads/{branch}')
    # Obtener el árbol
    tree = project.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
    # Buscar ruta en el árbol
    sha = [x.sha for x in tree if x.path == path_name]
    if not sha:
        # SHA no encontrado
        return None
    # SHA encontrado
    return project.get_git_blob(sha[0])

def getFileContent(project, filePath, boGitHub):
    if boGitHub:
        try:
            #res = project.get_contents(filePath)
            res = ghs.getContents(project, filePath)
            if isinstance(res, list):
                fileList = []
                for r in res:
                    #res2 = project.get_contents(r.path)
                    res2 = ghs.getContents(project, r.path)
                    if not isinstance(res2, list):
                        extension = r.path.split(".")[len(r.path.split("."))-1]
                        fileObj = ymlp.FileObj()
                        fileObj.setExtension(extension)
                        b = base64.b64decode(res2.content)
                        str_res = b.decode("utf-8")
                        fileObj.setContent(str(str_res))
                        fileList.append(fileObj)
                return fileList
            else:
                return str(res.decoded_content)
        except GithubException:
            blob = getBlobContent(project, "master", filePath)
            b64 = base64.b64decode(blob.content)
            content = b64.decode("utf8")
            return str(content)
    else:
        try:
            res = project.files.get(file_path=filePath, ref='master')
            b = base64.b64decode(res.content)
            str_res = b.decode("utf-8")
            return str(str_res)
        except:
            try:
                res = project.repository_tree(filePath)
                fileList = []
                for r in res:
                    rPath = r['path']
                    rName = r['name']
                    if gls.isFile(project,rPath):
                        extension = rPath.split(".")[len(rPath.split("."))-1]
                        fileObj = ymlp.FileObj()
                        fileObj.setExtension(extension)
                        resFile = project.files.get(file_path=rPath, ref='master')
                        b = base64.b64decode(resFile.content)
                        str_res = b.decode("utf-8")
                        fileObj.setContent(str(str_res))
                        fileList.append(fileObj)
                return fileList
            except:
                return ""

def getStrToFile(content):
    '''CASOS MUY CONCRETOS'''
    content = content.replace("node","_node")
    content = content.replace("new","_new")
    #content = content.replace("'*'","_*")

    '''RESTO'''
    content = content.replace("b''","")
    content = content.replace("b'","")
    #content = content.replace("'","")
    content = content.replace("\\\\n","\\_n")
    content = content.replace("\\n","\n")
    content = content.replace("\\\"","")
    content = content.replace("\\\\","")
    content = content.replace("`","")

    #content = content.replace("_*", "'*'")
    
    parts = content.split("\n")

    #PARA QUITARLE LA COMILLA DEL FINAL
    lastE = parts[len(parts)-1]
    '''lastE_aux = lastE.strip()[len(lastE.strip())-1]
    if lastE_aux == "'":'''
    parts[len(parts)-1] = lastE[0:len(lastE)-1]
    r = []
    for part in parts:
        part_aux = part.strip()
        if len(part_aux)>1 or (len(part_aux)<=1 and part_aux != '.'):
            r.append(part)

    return r
        
