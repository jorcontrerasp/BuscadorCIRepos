#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import pandas as pd
import herramientasCI as ci
import auxiliares as aux
import logging

def generarDataFrame(listaRepositorios, boEsGithub):
    aux.printLog("Generando DataFrame...", logging.INFO)
    repo1 = listaRepositorios[0]

    if boEsGithub:
        identificador = repo1.full_name
        url1 = repo1.html_url
        language1 = repo1.language
    else:
        identificador = repo1.attributes['path_with_namespace']
        url1 = repo1.attributes['web_url']
        language1 = ','.join(repo1.languages())

    df = pd.DataFrame([],
                      index=[identificador],
                      columns=["URL", "Lenguaje"
                                ,ci.HerramientasCI.CI1.value
                                , ci.HerramientasCI.CI2.value
                                , ci.HerramientasCI.CI3.value
                                , ci.HerramientasCI.CI4.value
                                , ci.HerramientasCI.CI5.value
                                , ci.HerramientasCI.CI6.value
                                , ci.HerramientasCI.CI7.value
                                , ci.HerramientasCI.CI8.value
                                , ci.HerramientasCI.CI9.value
                                , ci.HerramientasCI.CI10.value
                                , ci.HerramientasCI.CI11.value
                                , ci.HerramientasCI.CI12.value
                                , ci.HerramientasCI.CI13.value
                               ])
    df.at[identificador, "URL"] = url1
    df.at[identificador, "Lenguaje"] = language1
    df.at[identificador, ci.HerramientasCI.CI1.value] = " "
    df.at[identificador, ci.HerramientasCI.CI2.value] = " "
    df.at[identificador, ci.HerramientasCI.CI3.value] = " "
    df.at[identificador, ci.HerramientasCI.CI4.value] = " "
    df.at[identificador, ci.HerramientasCI.CI5.value] = " "
    df.at[identificador, ci.HerramientasCI.CI6.value] = " "
    df.at[identificador, ci.HerramientasCI.CI7.value] = " "
    df.at[identificador, ci.HerramientasCI.CI8.value] = " "
    df.at[identificador, ci.HerramientasCI.CI9.value] = " "
    df.at[identificador, ci.HerramientasCI.CI10.value] = " "
    df.at[identificador, ci.HerramientasCI.CI11.value] = " "
    df.at[identificador, ci.HerramientasCI.CI12.value] = " "
    df.at[identificador, ci.HerramientasCI.CI13.value] = " "

    for repo in listaRepositorios[1:len(listaRepositorios)]:

        if boEsGithub:
            identificador = repo.full_name
            url = repo.html_url
            language = repo.language
        else:
            identificador = repo.attributes['path_with_namespace']
            url = repo.attributes['web_url']
            language = ','.join(repo.languages())

        df2 = pd.DataFrame([],
                          index=[identificador],
                          columns=["URL", "Lenguaje"
                                    , ci.HerramientasCI.CI1.value
                                    , ci.HerramientasCI.CI2.value
                                    , ci.HerramientasCI.CI3.value
                                    , ci.HerramientasCI.CI4.value
                                    , ci.HerramientasCI.CI5.value
                                    , ci.HerramientasCI.CI6.value
                                    , ci.HerramientasCI.CI7.value
                                    , ci.HerramientasCI.CI8.value
                                    , ci.HerramientasCI.CI9.value
                                    , ci.HerramientasCI.CI10.value
                                    , ci.HerramientasCI.CI11.value
                                    , ci.HerramientasCI.CI12.value
                                    , ci.HerramientasCI.CI13.value
                                   ])
        df2.at[identificador, "URL"] = url
        df2.at[identificador, "Lenguaje"] = language
        df2.at[identificador, ci.HerramientasCI.CI1.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI2.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI3.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI4.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI5.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI6.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI7.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI8.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI9.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI10.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI11.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI12.value] = " "
        df2.at[identificador, ci.HerramientasCI.CI13.value] = " "
        df = df.append(df2)

    return df

def actualizarDataFrame(repo, literal, herramientaCI, boEsGithub, df):
    if boEsGithub:
        identificador = repo.full_name
    else:
        identificador = repo.attributes['path_with_namespace']
    valor = str(df.at[identificador, herramientaCI.value])
    if valor == " " or valor == "nan":
        df.at[identificador, herramientaCI.value] = "[" + literal + "]\n"
    else:
        df.at[identificador, herramientaCI.value] += "[" + literal + "]\n"

def generarDataFrameContadores():
    aux.printLog("Generando DataFrame contadores...", logging.INFO)
    df = pd.DataFrame([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      index=[ci.HerramientasCI.CI1.value
                            , ci.HerramientasCI.CI2.value
                            , ci.HerramientasCI.CI3.value
                            , ci.HerramientasCI.CI4.value
                            , ci.HerramientasCI.CI5.value
                            , ci.HerramientasCI.CI6.value
                            , ci.HerramientasCI.CI7.value
                            , ci.HerramientasCI.CI8.value
                            , ci.HerramientasCI.CI9.value
                            , ci.HerramientasCI.CI10.value
                            , ci.HerramientasCI.CI11.value
                            , ci.HerramientasCI.CI12.value
                            ,"Totales"],
                      columns=['Encontrados'])
    return df

def actualizarDataFrameContadores(fila, df):
    df.at[fila, "Encontrados"] += 1

def actualizarTotalesDataFrameContadores(df,df2):
    totales = contarRepositoriosAlMenos1Encontrado(df)
    df2.at["Totales", "Encontrados"] = totales

def contarRepositoriosAlMenos1Encontrado(df):
    cont = 0
    for index, row in df.iterrows():
        if (len(str(row[ci.HerramientasCI.CI1.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI2.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI3.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI4.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI5.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI6.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI7.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI8.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI9.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI10.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI11.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI12.value])) > 1):
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI13.value])) > 1):
            cont += 1
    return cont

def generarEXCEL(df, pFichero):
    aux.printLog("Generando fichero Excel...", logging.INFO)
    df.to_excel(pFichero + ".xlsx")

def generarCSV(df, pFichero):
    aux.printLog("Generando fichero Csv...", logging.INFO)
    df.to_csv(pFichero + ".csv")