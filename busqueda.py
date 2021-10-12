#AQUÍ se definirán las funciones de búsqueda.

def busquedaGitHubApiRepos(listaRepositorios, df, df2):
    listaEncontrados = []
    for repo in listaRepositorios:
        encontrado = buscarEnRepo(repo, "Criterios.criterio1.value", df)

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
