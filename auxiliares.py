#AQUÍ se definirán las funciones auxiliares del programa.

#Importamos las librerías necesarias.
import pickle
import datetime
import logging

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
