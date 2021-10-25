#AQUÍ se definirán las funciones de búsqueda.

#Importamos las librerías necesarias.
import auxiliares as aux
import herramientasCI as ci
import datos as d

def busquedaGitHubApiRepos(listaRepositorios, df):
    listaEncontrados = []
    for repo in listaRepositorios:
        encontrado1 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI1, [], df)
        encontrado2 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI2, [], df)
        encontrado3 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI3, [], df)
        encontrado4 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI4, [], df)
        encontrado5 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI5, [], df)
        encontrado6 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI6, [], df)
        encontrado7 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI7, [], df)
        encontrado8 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI8, [], df)
        encontrado9 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI9, [], df)
        encontrado10 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI10, [], df)
        encontrado11 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI11, [], df)
        encontrado12 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI12, [], df)
        encontrado13 = buscarRutaLiteralDesdeRaiz(repo, ci.HerramientasCI.CI13, [], df)

        # Si lo ha encontrado:
        # - lo añadimos a la listaEncontrados.
        encontrado = encontrado1 or encontrado2 or encontrado3 or encontrado4 or encontrado5 or encontrado6 or encontrado7 \
                     or encontrado8 or encontrado9 or encontrado10 or encontrado11 or encontrado12 or encontrado13
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

def buscarRutaLiteralDesdeRaiz(repo, herramientaCI, literales, df):
    try:
        if len(literales)==0:
            literales = ci.getFicherosBusquedaCI(herramientaCI.value)

        ruta = literales.pop(0)
        repo.get_contents(ruta)
        d.actualizarDataFrame(repo, ruta, herramientaCI, df)
        return True
    except:
        if len(literales)>0:
            return buscarRutaLiteralDesdeRaiz(repo, herramientaCI, literales, df)
        else:
            return False

def buscarRutaLiteralDesdeRaiz2(repo, ruta):
    try:
        repo.get_contents(ruta)
        return True
    except:
        return False

def buscarRutaLiteralDesdeRaiz3(repo, contents, literal):
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
