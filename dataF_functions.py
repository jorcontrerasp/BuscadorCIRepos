#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import string
import pandas as pd
import aux_functions as aux
import ci_yml_parser as ymlp
import gitlab_search as gls
import ci_tools as ci
import logging
import os

def getResultDFColumns():
    _columns = []
    _columns.append("URL")
    _columns.append("Lenguaje")
    _columns.append("N_CI_+")
    for ciTool in ci.getCIToolsValueList():
        _columns.append(ciTool)

    _columns.append("STAGES")
    _columns.append("NUM_JOBS")
    _columns.append("TOTAL_TASKS")
    _columns.append("TASK_AVERAGE_PER_JOB")
    
    return _columns

def getStatisticsDFColumns():
    _columns = []
    _columns.append("Num_repos")
    _columns.append("Total_jobs")
    _columns.append("Min")
    _columns.append("Max")
    _columns.append("Media")
    _columns.append("Mediana")

    return _columns

def getStageStatisticsDFColumns():
    _columns = []
    _columns.append("Num_projects_using")
    _columns.append("Total_stages")

    return _columns

def initDF(df, id, columns, initValue):
    try:
        id_str = str(id)
        for c in columns:
            c_str = str(c)
            df.at[id_str, c_str] = initValue
    except:
        print("ERROR indexing " + str(id))

def existsDFRecord(id, df):
        try:
            str_id = str(id)
            df.loc[str_id.lower()]
            return True
        except:
            return False

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
        language1 = ','.join(gls.getBackendLanguages(repo1.languages()))

    id = id.lower()

    df = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df, id, _columns, " ")
    df.at[id, "URL"] = url1
    df.at[id, "Lenguaje"] = language1
    df.at[id, "N_CI_+"] = 0
    df.at[id, "STAGES"] = " "
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
            language = ','.join(gls.getBackendLanguages(repo.languages()))

        id = id.lower()

        df2 = pd.DataFrame([],index=[id],columns=_columns)
        initDF(df2, id, _columns, " ")
        df2.at[id, "URL"] = url
        df2.at[id, "Lenguaje"] = language
        df2.at[id, "N_CI_+"] = 0
        df2.at[id, "STAGES"] = " "
        df2.at[id, "NUM_JOBS"] = 0
        df2.at[id, "TOTAL_TASKS"] = 0
        df2.at[id, "TASK_AVERAGE_PER_JOB"] = 0
        df = df.append(df2)

    return df

def makeEmptyDataFrame():
    aux.printLog("Generando DataFrame vacío...", logging.INFO)
    _columns = getResultDFColumns()
    df = pd.DataFrame([],index=[],columns=_columns)

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
        language = ','.join(gls.getBackendLanguages(repo.languages()))

    id = id.lower()

    df2 = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df2, id, _columns, " ")
    df2.at[id, "URL"] = url
    df2.at[id, "Lenguaje"] = language
    df2.at[id, "N_CI_+"] = 0
    df2.at[id, "STAGES"] = " "
    df2.at[id, "NUM_JOBS"] = 0
    df2.at[id, "TOTAL_TASKS"] = 0
    df2.at[id, "TASK_AVERAGE_PER_JOB"] = 0
    df = df.append(df2)

    return df

def updateDataFrameCiColumn(repo, literal, CITool, boGitHub, df):
    if boGitHub:
        id = repo.full_name
    else:
        id = repo.attributes['path_with_namespace']

    id = id.lower()

    df.at[id, CITool.value] = literal
    
    return df

def updateDataFrameCiObj(repo, ciObj, boGitHub, df, df6, lStagesProjectAdded):
    if boGitHub:
        id = repo.full_name
    else:
        id = repo.attributes['path_with_namespace']

    id = id.lower()

    ciObjType = type(ciObj)
    if isinstance(ciObj, ymlp.CIObj):
        lStages = []
        stages = ciObj.getStages()
        str_stages = str(stages).lower()
        if len(stages) == 1 and "?" in stages:
            jobs = ciObj.getJobs()
            for job in jobs:
                stageJob = job.getStage()
                if len(stageJob)>0:
                    lStages.append(str(stageJob).lower())
        elif isinstance(stages, list):
            for stage in stages:
                if len(stage)>0:
                    lStages.append(str(stage).lower())
        else:
            if len(stages)>0:
                lStages.append(str(stages).lower())

        if len(str(df.at[id, "STAGES"]))<=1:
            df.at[id, "STAGES"] = str(lStages)
        else:
            df.at[id, "STAGES"] += "\n" + str(lStages)

        df6,lStagesProjectAdded = updateStageStatisticsDF(lStages, df6, lStagesProjectAdded)

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
    
    return df,df6,lStagesProjectAdded

def doAuxWithResultsDF(df, df2, boGitHub):
    counterColumn = ""
    if boGitHub:
        counterColumn = "Encontrados_GitHub"
    else:
        counterColumn = "Encontrados_GitLab"
    df = updateDataFrameNumPositivesCIs(df)
    df2 = updateTotalCounterDataFrame(counterColumn, df, df2)
    df4,df5 = makeLanguageAndCIStatisticsDF(df,boGitHub)

    return df,df2,df4,df5

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

def add1CounterDFRecord(fila, column, df):
    df.at[fila, column] += 1
    return df

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

def updateTotalCounterDataFrame(column,df,df2):
    totales = countRepos1FoundUnless(df)
    df2.at["Totales", column] = totales
    return df2

def makeEmptyLanguageDataFrame():
    aux.printLog("Generando DataFrame por lenguajes vacío...", logging.INFO)
    _columns = ci.getCIToolsValueList()
    df = pd.DataFrame([],index=[],columns=_columns)

    return df

def addLanguageDFRecord(language, df):
    _columns = ci.getCIToolsValueList()
    df2 = pd.DataFrame([],index=[language],columns=_columns)
    initDF(df2, language, _columns, 0)
    df = df.append(df2)

    return df

def updateDataFrameNumPositivesCIs(df):
    pValue = "***"
    for index, row in df.iterrows():
        cont = 0
        if row[ci.HerramientasCI.CI1.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI2.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI3.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI4.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI5.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI6.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI7.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI8.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI9.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI10.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI11.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI12.value] == pValue:
            cont += 1
        if row[ci.HerramientasCI.CI13.value] == pValue:
            cont += 1
        
        df.at[index, "N_CI_+"] = cont

    return df

def makeLanguageAndCIStatisticsDF(resultsDF, boGitHub):
    pValue = "***"

    aux.printLog("Generando DataFrame de estadísticas por lenguaje...", logging.INFO)
    _columns = getStatisticsDFColumns()
    df1 = pd.DataFrame([],index=[],columns=_columns)

    aux.printLog("Generando DataFrame de estadísticas por CI...", logging.INFO)
    _columns = getStatisticsDFColumns()
    df2 = pd.DataFrame([],index=[],columns=_columns)
    df2 = addStatisticsDFRecord(df2, ci.HerramientasCI.CI2.value)
    df2 = addStatisticsDFRecord(df2, ci.HerramientasCI.CI4.value)
    df2 = addStatisticsDFRecord(df2, ci.HerramientasCI.CI8.value)

    for index,row in resultsDF.iterrows():
        language = row["Lenguaje"]

        if not isinstance(language, str):
            language = "EMPTY"
            aux.writeInLogFile("EMPTY language in proyect: " + index)

        if boGitHub:
            id = language
        else:
            id = gls.getFirstBackendLanguage(language.split(","))

        id = id.lower()

        if str(id) != "None" and len(str(id))>0 and id != ' ':
            if not existsDFRecord(id, df1):
                df1 = addStatisticsDFRecord(df1, id)
            
            df1 = updateDataFrameStatistics(df1, id, row)

        boTravis = row[ci.HerramientasCI.CI2.value] == pValue
        boGitHubActions = row[ci.HerramientasCI.CI4.value] == pValue
        boGitLabCI = row[ci.HerramientasCI.CI8.value] == pValue
        
        if boTravis:
            id = ci.HerramientasCI.CI2.value.lower()
            df2 = updateDataFrameStatistics(df2, id, row)
        
        if boGitHubActions:
            id = ci.HerramientasCI.CI4.value.lower()
            df2 = updateDataFrameStatistics(df2, id, row)
        
        if boGitLabCI:
            id = ci.HerramientasCI.CI8.value.lower()
            df2 = updateDataFrameStatistics(df2, id, row)
    
    # HACER MEDIA.
    df1 = updateStaticsDFJobAverage(df1)
    df2 = updateStaticsDFJobAverage(df2)

    return df1,df2
        

def addStatisticsDFRecord(df, id):
    id = id.lower()
    _columns = getStatisticsDFColumns()
    df2 = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df2, id, _columns, 0)
    df = df.append(df2)

    return df

def updateDataFrameStatistics(df, id, row):
    df.at[id, "Num_repos"] += 1
    nJobs = row["NUM_JOBS"]
    df.at[id, "Total_jobs"] += nJobs

    minJobs = df.at[id, "Min"]
    if minJobs == 0:
        df.at[id, "Min"] = nJobs
    elif(nJobs > 0 and nJobs < minJobs):
        df.at[id, "Min"] = nJobs
    
    maxJobs = df.at[id, "Max"]
    if(nJobs > 0 and nJobs > maxJobs):
        df.at[id, "Max"] = nJobs

    df.at[id, "Media"] = 0
    df.at[id, "Mediana"] = 0

    return df

def updateStaticsDFJobAverage(df):
    for index,row in df.iterrows():
        if index != "pd_empty_record":
            nRepos = row["Num_repos"]
            tJobs = row["Total_jobs"]
            jobAverage = 0
            if nRepos>0:
                jobAverage = tJobs/nRepos
            df.at[index, "Media"] = jobAverage
    
    return df

def makeEmptyStageStatisticsDataFrame():
    aux.printLog("Generando DataFrame vacío de estadísticas de 'stages'...", logging.INFO)
    _columns = getStageStatisticsDFColumns()
    df = pd.DataFrame([],index=[],columns=_columns)

    return df

def addStageStatisticsDFRecord(df, id):
    id = id.lower()
    _columns = getStageStatisticsDFColumns()
    df2 = pd.DataFrame([],index=[id],columns=_columns)
    initDF(df2, id, _columns, 0)
    df = df.append(df2)

    return df

def updateStageStatisticsDF(lStage, df, lStagesProjectAdded):
    if isinstance(lStage, list):
        dfAux = makeEmptyStageStatisticsDataFrame()
        for stage in lStage:
            if isinstance(stage, str):
                if not existsDFRecord(stage, dfAux):
                    dfAux = addStageStatisticsDFRecord(dfAux, stage)
                    dfAux.at[stage, "Num_projects_using"] += 1
                    dfAux.at[stage, "Total_stages"] += 1
                else:
                    dfAux.at[stage, "Total_stages"] += 1
        
        for index, row in dfAux.iterrows():
            if not existsDFRecord(index, df):
                df = addStageStatisticsDFRecord(df, index)
                df.at[index, "Num_projects_using"] += 1
            else:
                if not (index in lStagesProjectAdded):
                    df.at[index, "Num_projects_using"] += 1
                    lStagesProjectAdded.append(index)

            df.at[index, "Total_stages"] += dfAux.at[index, "Total_stages"]

    else:
        if isinstance(lStage, str):
            if not existsDFRecord(lStage, df):
                df = addStageStatisticsDFRecord(df, lStage)
                df.at[lStage, "Num_projects_using"] += 1
            else:
                if not (index in lStagesProjectAdded):
                    df.at[index, "Num_projects_using"] += 1
                    lStagesProjectAdded.append(index)

            df.at[lStage, "Total_stages"] += 1
    
    return df,lStagesProjectAdded

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