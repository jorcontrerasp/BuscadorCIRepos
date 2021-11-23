#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import pandas as pd
import herramientasCI as ci
import auxiliares as aux
import logging
import os

def makeDataFrame(lRepositories, boGitHub):
    aux.printLog("Generando DataFrame...", logging.INFO)
    repo1 = lRepositories[0]

    if boGitHub:
        id = repo1.full_name
        url1 = repo1.html_url
        language1 = repo1.language
    else:
        id = repo1.attributes['path_with_namespace']
        url1 = repo1.attributes['web_url']
        language1 = ','.join(repo1.languages())

    df = pd.DataFrame([],
                      index=[id],
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
    df.at[id, "URL"] = url1
    df.at[id, "Lenguaje"] = language1
    df.at[id, ci.HerramientasCI.CI1.value] = " "
    df.at[id, ci.HerramientasCI.CI2.value] = " "
    df.at[id, ci.HerramientasCI.CI3.value] = " "
    df.at[id, ci.HerramientasCI.CI4.value] = " "
    df.at[id, ci.HerramientasCI.CI5.value] = " "
    df.at[id, ci.HerramientasCI.CI6.value] = " "
    df.at[id, ci.HerramientasCI.CI7.value] = " "
    df.at[id, ci.HerramientasCI.CI8.value] = " "
    df.at[id, ci.HerramientasCI.CI9.value] = " "
    df.at[id, ci.HerramientasCI.CI10.value] = " "
    df.at[id, ci.HerramientasCI.CI11.value] = " "
    df.at[id, ci.HerramientasCI.CI12.value] = " "
    df.at[id, ci.HerramientasCI.CI13.value] = " "

    for repo in lRepositories[1:len(lRepositories)]:

        if boGitHub:
            id = repo.full_name
            url = repo.html_url
            language = repo.language
        else:
            id = repo.attributes['path_with_namespace']
            url = repo.attributes['web_url']
            language = ','.join(repo.languages())

        df2 = pd.DataFrame([],
                          index=[id],
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
        df2.at[id, "URL"] = url
        df2.at[id, "Lenguaje"] = language
        df2.at[id, ci.HerramientasCI.CI1.value] = " "
        df2.at[id, ci.HerramientasCI.CI2.value] = " "
        df2.at[id, ci.HerramientasCI.CI3.value] = " "
        df2.at[id, ci.HerramientasCI.CI4.value] = " "
        df2.at[id, ci.HerramientasCI.CI5.value] = " "
        df2.at[id, ci.HerramientasCI.CI6.value] = " "
        df2.at[id, ci.HerramientasCI.CI7.value] = " "
        df2.at[id, ci.HerramientasCI.CI8.value] = " "
        df2.at[id, ci.HerramientasCI.CI9.value] = " "
        df2.at[id, ci.HerramientasCI.CI10.value] = " "
        df2.at[id, ci.HerramientasCI.CI11.value] = " "
        df2.at[id, ci.HerramientasCI.CI12.value] = " "
        df2.at[id, ci.HerramientasCI.CI13.value] = " "
        df = df.append(df2)

    return df

def updateDataFrame(repo, literal, CITool, boGitHub, df):
    if boGitHub:
        id = repo.full_name
    else:
        id = repo.attributes['path_with_namespace']
    value = str(df.at[id, CITool.value])
    if value == " " or value == "nan":
        df.at[id, CITool.value] = "[" + literal + "]\n"
    else:
        df.at[id, CITool.value] += "[" + literal + "]\n"

def makeCounterDataFrame():
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

def updateCounterDataFrame(fila, df):
    df.at[fila, "Encontrados"] += 1

def updateTotalCounterDataFrame(df,df2):
    totales = countRepos1FoundUnless(df)
    df2.at["Totales", "Encontrados"] = totales

def countRepos1FoundUnless(df):
    cont = 0
    for index, row in df.iterrows():
        if (len(str(row[ci.HerramientasCI.CI1.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI1.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI2.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI2.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI3.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI3.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI4.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI4.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI5.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI5.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI6.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI6.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI7.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI7.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI8.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI8.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI9.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI9.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI10.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI10.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI11.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI11.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI12.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI12.value]:
            cont += 1
        elif (len(str(row[ci.HerramientasCI.CI13.value])) > 1) and "EXCEPT" not in row[ci.HerramientasCI.CI13.value]:
            cont += 1
    return cont

def makeEXCEL(df, pFile):
    aux.printLog("Generando fichero Excel...", logging.INFO)
    folder = "results"
    if not os.path.exists(folder):
        os.mkdir(folder)
    df.to_excel(folder + "/" + pFile + ".xlsx")

def makeCSV(df, pFile):
    aux.printLog("Generando fichero Csv...", logging.INFO)
    folder = "results"
    if not os.path.exists(folder):
        os.mkdir(folder)
    df.to_csv(folder + "/" + pFile + ".csv")