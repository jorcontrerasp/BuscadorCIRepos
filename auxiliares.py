#AQUÍ se definirán las funciones auxiliares del programa.

#Importamos las librerías necesarias.
import pickle
import datetime
import logging

def generarPickle(nombreFichero, listaRepositorios):
    printLog("Generando fichero pickle...", logging.INFO)
    with open(nombreFichero, 'wb') as f:
        pickle.dump(listaRepositorios, f)
    printLog("Fichero " + nombreFichero + " generado", logging.INFO)

def cargarRepositorios(fichero):
    printLog("Cargando repositorios...", logging.INFO)
    with open(fichero, 'rb') as f:
        repositories = pickle.load(f)
    return repositories

def imprimirListaGitHubRepos(repositorios):
    print("Lista de repositorios: ")
    for project in repositorios:
        project_name = project.full_name.split("/")[1]
        print(project.full_name)

def imprimirListaGitLabRepos(proyectos):
    print("Lista de proyectos: ")
    for project in proyectos:
        print(project.attributes['path_with_namespace'])

def obtenerFicheroIt(path):
    if "/" in path:
        pathArray = path.split("/")
        fActual = pathArray[len(pathArray) - 1]
    else:
        fActual = path
    return fActual

def leerFichero(fichero):
    with open(fichero, 'rb') as f:
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
