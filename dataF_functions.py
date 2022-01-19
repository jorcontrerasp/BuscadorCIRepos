#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import pandas as pd
import ci_tools as ci
import aux_functions as aux
import logging
import os
import ci_yml_parser as ymlp

def getResultDFColumns():
    _columns = []
    _columns.append("URL")
    _columns.append("Lenguaje")
    for ciTool in ci.getCIToolsValueList():
        _columns.append(ciTool)

    _columns.append("STAGES")
    _columns.append("NUM_JOBS")
    _columns.append("TOTAL_TASKS")
    _columns.append("TASK_AVERAGE_PER_JOB")
    
    return _columns

def initDF(df, id, columns, initValue):
    for c in columns:
        df.at[id, c] = initValue

def makeDataFrame(lRepositories, boGitHub):
    aux.printLog("Generando DataFrame...", logging.INFO)
    _columns = getResultDFColumns()
    repo1 = lRepositories[0]

    if boGitHub:
        id = repo1.full_name
        url1 = repo1.html_url
        language1 = repo1.language
    else:
        id = repo1.attributes['path_with_namespace']
        url1 = repo1.attributes['web_url']
        language1 = ','.join(repo1.languages())

    df = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df, id, _columns, " ")
    df.at[id, "URL"] = url1
    df.at[id, "Lenguaje"] = language1
    df.at[id, "STAGES"] = 0
    df.at[id, "NUM_JOBS"] = 0
    df.at[id, "TOTAL_TASKS"] = 0
    df.at[id, "TASK_AVERAGE_PER_JOB"] = 0

    for repo in lRepositories[1:len(lRepositories)]:
        if boGitHub:
            id = repo.full_name
            url = repo.html_url
            language = repo.language
        else:
            id = repo.attributes['path_with_namespace']
            url = repo.attributes['web_url']
            language = ','.join(repo.languages())

        df2 = pd.DataFrame([],index=[id],columns=_columns)
        initDF(df2, id, _columns, " ")
        df2.at[id, "URL"] = url
        df2.at[id, "Lenguaje"] = language
        df2.at[id, "STAGES"] = 0
        df2.at[id, "NUM_JOBS"] = 0
        df2.at[id, "TOTAL_TASKS"] = 0
        df2.at[id, "TASK_AVERAGE_PER_JOB"] = 0
        df = df.append(df2)

    return df

def makeEmptyDataFrame():
    aux.printLog("Generando DataFrame vacío...", logging.INFO)
    id = "EmptyRecord"
    _columns = getResultDFColumns()
    df = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df, id, _columns, " ")

    df.at[id, "STAGES"] = 0
    df.at[id, "NUM_JOBS"] = 0
    df.at[id, "TOTAL_TASKS"] = 0
    df.at[id, "TASK_AVERAGE_PER_JOB"] = 0

    return df

def addDFRecord(repo, df, boGitHub):
    _columns = getResultDFColumns()
    if boGitHub:
        id = repo.full_name
        url = repo.html_url
        language = repo.language
    else:
        id = repo.attributes['path_with_namespace']
        url = repo.attributes['web_url']
        language = ','.join(repo.languages())
        
    df2 = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df2, id, _columns, " ")
    df2.at[id, "URL"] = url
    df2.at[id, "Lenguaje"] = language
    df2.at[id, "STAGES"] = 0
    df2.at[id, "NUM_JOBS"] = 0
    df2.at[id, "TOTAL_TASKS"] = 0
    df2.at[id, "TASK_AVERAGE_PER_JOB"] = 0
    df = df.append(df2)

    return df

def makeCounterDataFrame():
    aux.printLog("Generando DataFrame contadores...", logging.INFO)
    columna1 = "Encontrados_GitHub"
    columna2 = "Encontrados_GitLab"
    _index = ci.getCIToolsValueList()
    _index.append("Totales")
    df = pd.DataFrame([],index=_index,columns=[columna1, columna2])

    for i in _index:
        df.at[i, columna1] = 0

    for i in _index:
        df.at[i, columna2] = 0

    return df

def makeEmptyLanguageDataFrame():
    aux.printLog("Generando DataFrame por lenguajes vacío...", logging.INFO)
    id = "EmptyRecord"
    _columns = ci.getCIToolsValueList()
    df = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df, id, _columns, 0)

    return df

def addLanguageDFRecord(language, df):
    _columns = ci.getCIToolsValueList()
    df2 = pd.DataFrame([],index=[language],columns=_columns)
    initDF(df2, language, _columns, 0)
    df = df.append(df2)

    return df

def updateDataFrameCiColumn(repo, literal, CITool, boGitHub, df):
    if boGitHub:
        id = repo.full_name
    else:
        id = repo.attributes['path_with_namespace']

    df.at[id, CITool.value] = literal
    
    return df

def updateDataFrameCiObj(repo, ciObj, boGitHub, df):
    if boGitHub:
        id = repo.full_name
    else:
        id = repo.attributes['path_with_namespace']

    ciObjType = type(ciObj)
    if isinstance(ciObj, ymlp.CIObj):
        if len(str(df.at[id, "STAGES"]))<=1:
            df.at[id, "STAGES"] = str(ciObj.getStages())
        else:
            df.at[id, "STAGES"] += "\n" + str(ciObj.getStages())

        df.at[id, "NUM_JOBS"] += len(ciObj.getJobs())

        nTasks = 0
        for job in ciObj.getJobs():
            nTasks += len(job.getTasks())

        df.at[id, "TOTAL_TASKS"] += nTasks

        tasks = df.at[id, "TOTAL_TASKS"]
        jobs = df.at[id, "NUM_JOBS"]
        if jobs == 0:
            taskAverage = -1
        else:
            taskAverage = tasks/jobs

        df.at[id, "TASK_AVERAGE_PER_JOB"] = taskAverage
    
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

def printDF(df):
    print("----------------------------------------------------------------------------------------------------")
    print(df)
    print("----------------------------------------------------------------------------------------------------")