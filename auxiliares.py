#AQUÍ se definirán las funciones auxiliares del programa.

#Importamos las librerías necesarias.
import pickle

def generarPickle(nombreFichero, listaRepositorios):
    print("Generando fichero pickle...")
    with open(nombreFichero, 'wb') as f:
        pickle.dump(listaRepositorios, f)
    print("Fichero " + nombreFichero + " generado")

def cargarRepositorios(fichero):
    print("Cargando repositorios...")
    with open(fichero, 'rb') as f:
        repositories = pickle.load(f)
    return repositories

def imprimirListaRepositorios(repositorios):
    print("Imprimiendo lista de repositorios...")
    for project in repositorios:
        project_name = project.full_name.split("/")[1]
        print(project.full_name)

def obtenerFicheroIt(path):
    if "/" in path:
        pathArray = path.split("/")
        fActual = pathArray[len(pathArray) - 1]
    else:
        fActual = path
    return fActual
