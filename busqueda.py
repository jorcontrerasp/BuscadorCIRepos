#AQUÍ se definirán las funciones de búsqueda.

#Importamos las librerías necesarias.
import auxiliares as aux

def busquedaGitHubApiRepos(listaRepositorios):
    listaEncontrados = []
    for repo in listaRepositorios:
        encontrado = buscarRutaLiteralDesdeRaiz(repo, ".bazelci/presubmit.yml")

        # Si lo ha encontrado:
        # - lo añadimos a la listaEncontrados.
        if encontrado:
            listaEncontrados.append(repo)

    return listaEncontrados

def buscarEnRepo(repo, literal):
    encontrado = False
    contents = repo.get_contents("")
    while contents:
        content_file = contents.pop(0)
        if literal in content_file.path.lower():
            encontrado = True
            print(str(content_file.path))
            break
        else:
            if content_file.type == "dir":
                contents.extend(repo.get_contents(content_file.path))
    return encontrado

def buscarEnRaiz(repo, literal):
    encontrado = False
    contents = repo.get_contents("")
    for content_file in contents:
        if literal in content_file.path.lower():
            encontrado = True
            print(str(content_file.path))
            break
    return encontrado

def buscarRutaLiteralDesdeRaiz(repo, ruta):
    try:
        repo.get_contents(ruta)
        return True
    except:
        return False

def buscarRutaLiteralDesdeRaiz2(repo, contents, literal):
    encontrado = False
    pLiteral = literal.split("/")
    cLiteral = pLiteral.pop(0)
    for contentFile in contents:
        ficheroIt = aux.obtenerFicheroIt(contentFile.path)
        if cLiteral == ficheroIt.lower():
            if len(pLiteral) > 0:
                if contentFile.type == "dir":
                    contents = repo.get_contents(contentFile.path)
                    encontrado = buscarRutaLiteralDesdeRaiz(repo, contents, '/'.join(pLiteral))
                    break
            else:
                encontrado = True
    return encontrado
