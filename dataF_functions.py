#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import pandas as pd
import ci_tools as ci
import aux_functions as aux
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

def makeEmptyDataFrame():
    aux.printLog("Generando DataFrame vacío...", logging.INFO)
    id = "EmptyRecord"
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
    df.at[id, "URL"] = " "
    df.at[id, "Lenguaje"] = " "
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

    return df

def addDFRecord(repo, df, boGitHub):
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

    df.at[id, CITool.value] = literal
    
    return df

def getDF(df):
    return df

def printDF(df):
    print("----------------------------------------------------------------------------------------------------")
    print(df)
    print("----------------------------------------------------------------------------------------------------")

def makeCounterDataFrame():
    aux.printLog("Generando DataFrame contadores...", logging.INFO)
    df = pd.DataFrame([],
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
                            , ci.HerramientasCI.CI13.value
                            ,"Totales"],
                      columns=['Encontrados_GitHub', 'Encontrados_GitLab'])

    columna = "Encontrados_GitHub"
    df.at[ci.HerramientasCI.CI1.value, columna] = 0
    df.at[ci.HerramientasCI.CI2.value, columna] = 0
    df.at[ci.HerramientasCI.CI3.value, columna] = 0
    df.at[ci.HerramientasCI.CI4.value, columna] = 0
    df.at[ci.HerramientasCI.CI5.value, columna] = 0
    df.at[ci.HerramientasCI.CI6.value, columna] = 0
    df.at[ci.HerramientasCI.CI7.value, columna] = 0
    df.at[ci.HerramientasCI.CI8.value, columna] = 0
    df.at[ci.HerramientasCI.CI9.value, columna] = 0
    df.at[ci.HerramientasCI.CI10.value, columna] = 0
    df.at[ci.HerramientasCI.CI11.value, columna] = 0
    df.at[ci.HerramientasCI.CI12.value, columna] = 0
    df.at[ci.HerramientasCI.CI13.value, columna] = 0
    df.at["Totales", columna] = 0

    columna = "Encontrados_GitLab"
    df.at[ci.HerramientasCI.CI1.value, columna] = 0
    df.at[ci.HerramientasCI.CI2.value, columna] = 0
    df.at[ci.HerramientasCI.CI3.value, columna] = 0
    df.at[ci.HerramientasCI.CI4.value, columna] = 0
    df.at[ci.HerramientasCI.CI5.value, columna] = 0
    df.at[ci.HerramientasCI.CI6.value, columna] = 0
    df.at[ci.HerramientasCI.CI7.value, columna] = 0
    df.at[ci.HerramientasCI.CI8.value, columna] = 0
    df.at[ci.HerramientasCI.CI9.value, columna] = 0
    df.at[ci.HerramientasCI.CI10.value, columna] = 0
    df.at[ci.HerramientasCI.CI11.value, columna] = 0
    df.at[ci.HerramientasCI.CI12.value, columna] = 0
    df.at[ci.HerramientasCI.CI13.value, columna] = 0
    df.at["Totales", columna] = 0

    return df

def add1CounterDFRecord(fila, column, df):
    df.at[fila, column] += 1
    return df

def updateTotalCounterDataFrame(column,df,df2):
    totales = countRepos1FoundUnless(df)
    df2.at["Totales", column] = totales
    return df2

def countRepos1FoundUnless(df):
    cont = 0
    pValue = "***"
    for index, row in df.iterrows():
        if row[ci.HerramientasCI.CI1.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI2.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI3.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI4.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI5.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI6.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI7.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI8.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI9.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI10.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI11.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI12.value] == pValue:
            cont += 1
        elif row[ci.HerramientasCI.CI13.value] == pValue:
            cont += 1

    return cont

def existsDFRecord(id, df):
        try:
            df.at[id, ci.HerramientasCI.CI1.value]
            return True
        except:
            return False

def makeEmptyLanguageDataFrame():
    aux.printLog("Generando DataFrame por lenguajes vacío...", logging.INFO)
    id = "EmptyRecord"
    df = pd.DataFrame([],
                      index=[id],
                      columns=[ci.HerramientasCI.CI1.value
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

    df.at[id, ci.HerramientasCI.CI1.value] = 0
    df.at[id, ci.HerramientasCI.CI2.value] = 0
    df.at[id, ci.HerramientasCI.CI3.value] = 0
    df.at[id, ci.HerramientasCI.CI4.value] = 0
    df.at[id, ci.HerramientasCI.CI5.value] = 0
    df.at[id, ci.HerramientasCI.CI6.value] = 0
    df.at[id, ci.HerramientasCI.CI7.value] = 0
    df.at[id, ci.HerramientasCI.CI8.value] = 0
    df.at[id, ci.HerramientasCI.CI9.value] = 0
    df.at[id, ci.HerramientasCI.CI10.value] = 0
    df.at[id, ci.HerramientasCI.CI11.value] = 0
    df.at[id, ci.HerramientasCI.CI12.value] = 0
    df.at[id, ci.HerramientasCI.CI13.value] = 0

    return df

def addLanguageDFRecord(language, df):
        
    df2 = pd.DataFrame([],
                          index=[language],
                          columns=[ci.HerramientasCI.CI1.value
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

    df2.at[language, ci.HerramientasCI.CI1.value] = 0
    df2.at[language, ci.HerramientasCI.CI2.value] = 0
    df2.at[language, ci.HerramientasCI.CI3.value] = 0
    df2.at[language, ci.HerramientasCI.CI4.value] = 0
    df2.at[language, ci.HerramientasCI.CI5.value] = 0
    df2.at[language, ci.HerramientasCI.CI6.value] = 0
    df2.at[language, ci.HerramientasCI.CI7.value] = 0
    df2.at[language, ci.HerramientasCI.CI8.value] = 0
    df2.at[language, ci.HerramientasCI.CI9.value] = 0
    df2.at[language, ci.HerramientasCI.CI10.value] = 0
    df2.at[language, ci.HerramientasCI.CI11.value] = 0
    df2.at[language, ci.HerramientasCI.CI12.value] = 0
    df2.at[language, ci.HerramientasCI.CI13.value] = 0
    df = df.append(df2)

    return df

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