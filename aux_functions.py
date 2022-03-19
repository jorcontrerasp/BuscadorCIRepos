#AQUÍ se definirán las funciones auxiliares del programa.

#Importamos las librerías necesarias.
from github import GithubException
import ci_yml_parser as ymlp
import gitlab_search as gls
import github_search as ghs
import pickle
import datetime
import logging
import base64
import os

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

def printGitHubRepoList(repositories):
    print("Lista de repositorios: ")
    for project in repositories:
        projectName = project.full_name.split("/")[1]
        print(project.full_name)

def printGitLabProyectList(projects):
    print("Lista de proyectos: ")
    for project in projects:
        print(project.attributes['path_with_namespace'])

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

def writeInLogFile(mensaje):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    f = open("logs/f.log", "a")
    f.write(mensaje)
    f.write("\n")
    f.close

def getTimestamp():
    timestamp = str(datetime.datetime.now())[0:19]
    return timestamp

def getFileContent(project, filePath, boGitHub):
    if boGitHub:
        try:
            res = ghs.getContents(project, filePath)
            if isinstance(res, list):
                fileList = []
                for r in res:
                    res2 = ghs.getContents(project, r.path)
                    if not isinstance(res2, list):
                        extension = r.path.split(".")[len(r.path.split("."))-1]
                        fileObj = ymlp.FileObj()
                        fileObj.setExtension(extension)
                        b = base64.b64decode(res2.content)
                        str_res = b.decode("utf-8")
                        fileObj.setContent(decodeStr(str_res))
                        fileList.append(fileObj)
                return fileList
            else:
                return decodeStr(res.decoded_content)
        except GithubException:
            blob = getGitHubBlobContent(project, filePath)
            b64 = base64.b64decode(blob.content)
            content = b64.decode("utf8")
            return decodeStr(content)
    else:
        try:
            #res = project.files.get(file_path=filePath, ref='master')
            res = gls.getFile(project,filePath,None)
            if(str(res)!="None"):
                b = base64.b64decode(res.content)
                str_res = b.decode("utf-8")
                return decodeStr(str_res)
            else:
                return searchGitLabBlobContent(project,filePath)
        except:
            return searchGitLabBlobContent(project,filePath)

def getGitHubBlobContent(project, path_name):
    masterB = "master"
    try:
        # Obtener referencia del "branch"
        ref = project.get_git_ref(f'heads/{masterB}')
        # Obtener el árbol
        tree = project.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
        # Buscar ruta en el árbol
        sha = [x.sha for x in tree if x.path == path_name]
        if not sha:
            # SHA no encontrado
            return None
        # SHA encontrado
        return project.get_git_blob(sha[0])
    except:
        return searchGitHubBlobContentInBranches(project,path_name)
    
    return None

def searchGitHubBlobContentInBranches(project, path_name):
    branches = project.get_branches()
    for branch in branches:
        try:
            branchName = branch.name
            # Obtener referencia del "branch"
            ref = project.get_git_ref(f'heads/{branchName}')
            # Obtener el árbol
            tree = project.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
            # Buscar ruta en el árbol
            sha = [x.sha for x in tree if x.path == path_name]
            if not sha:
                # SHA no encontrado
                return None
            # SHA encontrado
            return project.get_git_blob(sha[0])
        except:
            continue

    return None

def searchGitLabBlobContent(project, filePath):
    try:
        res = project.repository_tree(filePath)
        fileList = []
        for r in res:
            rPath = r['path']
            rName = r['name']
            boFile,branch = gls.isFile(project,rPath, False)
            if boFile:
                extension = rPath.split(".")[len(rPath.split("."))-1]
                fileObj = ymlp.FileObj()
                fileObj.setExtension(extension)
                #resFile = project.files.get(file_path=rPath, ref='master')
                resFile = gls.getFile(project,rPath,branch)
                b = base64.b64decode(resFile.content)
                str_res = b.decode("utf-8")
                fileObj.setContent(decodeStr(str_res))
                fileList.append(fileObj)
        return fileList
    except:
        return ""

def decodeStr(value):
    r = ""
    try:
        r = value.decode()
    except:
        r = value
    return str(r)

def getStrToFile(content):

    content_aux = decodeStr(content)

    #CASOS MUY CONCRETOS
    content_aux = content_aux.replace("node","_node")
    content_aux = content_aux.replace("new","_new")
    content_aux = content_aux.replace("npm","_npm")
    content_aux = content_aux.replace("n24333f8a63b6825ea9c5514f83c2829b004d1fee","_n24333f8a63b6825ea9c5514f83c2829b004d1fee")
    content_aux = content_aux.replace("n8933bad161af4178b1185d1a37fbf41ea5269c55","_n8933bad161af4178b1185d1a37fbf41ea5269c55")
    content_aux = content_aux.replace("nd56f5187479451eabf01fb78af6dfcb131a6481e","_nd56f5187479451eabf01fb78af6dfcb131a6481e")
    content_aux = content_aux.replace("n84831b9409646a918e30573bab4c9c91346d8abd","_n84831b9409646a918e30573bab4c9c91346d8abd")
    content_aux = content_aux.replace("setup.py.\\n","setup.py.\\_n")

    #RESTO
    content_aux = content_aux.replace("\\n","\\_n")
    content_aux = content_aux.replace("\\\"","")
    content_aux = content_aux.replace("\\\\","")

    parts = content_aux.split("\n")

    #PARA QUITARLE LA COMILLA/ESPACIO DEL FINAL
    lastE = parts[len(parts)-1]
    if lastE != "":
        lastE2 = lastE[len(lastE)-1]
        if lastE2 == "'":
            lastEAux = lastE[0:len(lastE)-1]
            parts[len(parts)-1] = lastEAux
    else:
        lastEAux = lastE[0:len(lastE)-1]
        parts[len(parts)-1] = lastEAux
    #PARA QUITARLE LÍNEAS EN LAS QUE SOLO VENGA UN PUNTO
    r = []
    for part in parts:
        part_aux = part.strip()
        addToReturn = (len(part_aux)>1 or (len(part_aux)<=1 and part_aux != '.'))
        if addToReturn:
            r.append(part)
            
    return r
        
