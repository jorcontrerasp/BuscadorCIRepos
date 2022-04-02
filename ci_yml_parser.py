import ci_yml_parser as ymlp
import aux_functions as aux
import ci_tools as ci
import shutil
from shutil import rmtree
import logging
import yaml
import io
import os

# Puede darse el caso de que el "parseador" encuentre trabajos sin tarea (que no tenga etiquetas de script, install, etc.)
# Puede darse el caso de que el "parseador" encuentre trabajos sin stage definido con claridad (etiqueta on, stage/stages, etc.)

class FileObj:
    extension = ""
    content = ""

    def __init__(self) -> None:
        self.extension = ""
        self.content = ""

    # GETTER & SETTER
    def getExtension(self):
        return self.extension

    def setExtension(self, extension):
        self.extension = extension

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

class CIJob:
    stage = ""
    tasks = [] 
    
    def __init__(self) -> None:
        self.stage = ""
        self.tasks = []

    def CIJobToString(self):
        job_str = "CIJob:\n" + "\t\t\t- Stage: " + str(self.stage) + "\n\t\t\t- Tasks: "
        for task in self.tasks:
            job_str = job_str + "\n\t\t\t\t* " + str(task)

        job_str = job_str + "\n"
        return str(job_str)

    # GETTER & SETTER
    def getStage(self):
        return self.stage

    def setStage(self, stage):
        self.stage = stage

    def getTasks(self):
        return self.tasks

    def setTasks(self, tasks):
        self.tasks = tasks

class CIObj:
    ciTool = ""
    stages = []
    jobs = []

    def __init__(self) -> None:
        self.ciTool = ""
        self.stages = []
        self.jobs = []

    def CIObjToString(self):
        ci_str = "CIObj(" + str(self.ciTool) + "):\n" + "\t- Stages: " + str(self.stages) + "\n\t- Jobs: "
        for job in self.jobs:
            ci_str = ci_str + "\n\t\t> " + job.CIJobToString()

        ci_str = ci_str + "\n"
        return str(ci_str)

    # GETTER & SETTER
    def getCiTool(self):
        return self.ciTool

    def setCiTool(self, ciTool):
        self.ciTool = ciTool

    def getStages(self):
        return self.stages

    def setStages(self, stages):
        self.stages = stages

    def getJobs(self):
        return self.jobs

    def setJobs(self, jobs):
        self.jobs = jobs

def getParseObj(repo, path, CITool, boGitHub):
    ciObj = None
    ciObjList = []
    try:
        # Generamos el directorio 'tmp'
        if not os.path.exists(tmpDirectory):
            os.mkdir(tmpDirectory)

        doYMLParse = CITool.value == ci.HerramientasCI.CI2.value or CITool.value == ci.HerramientasCI.CI4.value or CITool.value == ci.HerramientasCI.CI8.value

        repoName = ""
        if boGitHub:
            repoName = repo.full_name
        else:
            repoName = repo.attributes['path_with_namespace']
        
        if doYMLParse:
            makeYMLTmpFile(repo, path, boGitHub)
            if os.path.exists(tmpFile):
                ciObj = CIObj()
                if CITool.value == ci.HerramientasCI.CI2.value:
                    ciObj = parseTravisYAML(tmpFile,repoName)
                    os.remove(tmpFile)
                elif CITool.value == ci.HerramientasCI.CI4.value:
                    ciObj = parseGitHubActionsYAML(tmpFile,repoName)
                    os.remove(tmpFile)
                elif CITool.value == ci.HerramientasCI.CI8.value:
                    ciObj = parseGitLabYAML(tmpFile,repoName)
                    os.remove(tmpFile)
                ciObj.setCiTool(CITool.value)
                if boPrintCIObjs:
                    print(ciObj.CIObjToString())
            else:
                if os.path.exists(tmpDirectory):
                    ymlFiles = os.listdir(tmpDirectory)
                    for ymlF in ymlFiles:
                        ymlF = tmpDirectory + "/" + ymlF
                        ciObj = CIObj()
                        if CITool.value == ci.HerramientasCI.CI2.value:
                            ciObj = parseTravisYAML(ymlF,repoName)
                            os.remove(ymlF)
                        elif CITool.value == ci.HerramientasCI.CI4.value:
                            ciObj = parseGitHubActionsYAML(ymlF,repoName)
                            os.remove(ymlF)
                        elif CITool.value == ci.HerramientasCI.CI8.value:
                            ciObj = parseGitLabYAML(ymlF,repoName)
                            os.remove(ymlF)
                        ciObj.setCiTool(CITool.value)
                        if boPrintCIObjs:
                            print(ciObj.CIObjToString())
                        ciObjList.append(ciObj)

    except:
        aux.printLog("No se ha podido parsear el fichero YML: '" + path + "'", logging.INFO)

    rmtree("./" + tmpDirectory)

    if len(ciObjList)>0:
        return ciObjList
    else:
        return ciObj

def parseGitLabYAML(yamlFile, repoName):
    dataLoaded = loadData(yamlFile,repoName)
    jobs = []
    stages = []
    strdl = str(dataLoaded)
    if not strdl == "None":
        stagesContent = getValueArrayParam(dataLoaded, 'stages')
        if len(stagesContent)==0:
            stages.append("?")
        elif isinstance(stagesContent, list) or isinstance(stagesContent, dict):
            for w in stagesContent:
                stages.append(w)
        else:
            stages.append(stagesContent)
        
        for topLevel in dataLoaded:

            topLevelContent = getValueArrayParam(dataLoaded, topLevel)
            stage = getValueArrayParam(topLevelContent, 'stage')
            script = getValueArrayParam(topLevelContent, 'script')

            if topLevel == "workflow":
                rules = getValueArrayParam(topLevelContent, 'rules')
                if len(rules)>0:
                    job = CIJob()
                    job.setStage(topLevel)
                    jobTasks = []
                    if isinstance(rules, list) or isinstance(rules, dict):
                        for rule in rules:
                            jobTasks.append(rule)
                    else:
                        jobTasks.append(rules)
                    job.setTasks(jobTasks)
                    jobs.append(job)
            elif topLevel in getMainYMLStages():
                job = CIJob()
                jobTasks = []
                jobStages = []
                jobStages.append(topLevel)
                job.setStage(jobStages)
                if len(script)>0:
                    if isinstance(script, list) or isinstance(script, dict):
                        for task in script:
                            jobTasks.append(task)
                    else:
                        jobTasks.append(script)
                else:
                    if isinstance(topLevelContent, list) or isinstance(topLevelContent, dict):
                        for task in topLevelContent:
                            jobTasks.append(task)
                    else:
                        jobTasks.append(topLevelContent)
                job.setTasks(jobTasks)
                jobs.append(job)
            elif len(script)>0:
                job = CIJob()
                jobStages = []
                if len(stage)==0:
                    '''jobStages.append(topLevel)'''
                    jobStages.append("script")
                else:
                    jobStages.append(stage)
                    
                job.setStage(jobStages)
                jobTasks = []
                if isinstance(script, list) or isinstance(script, dict):
                    for task in script:
                        jobTasks.append(task)
                else:
                    jobTasks.append(script)
                job.setTasks(jobTasks)
                jobs.append(job)
    ciObj = CIObj()
    ciObj.setStages(stages)
    ciObj.setJobs(jobs)
    return ciObj
    
def parseGitHubActionsYAML(yamlFile, repoName):
    # La etiqueta 'on' la detecta como True ¿?
    dataLoaded = loadData(yamlFile,repoName)
    jobs = []
    when = []
    strdl = str(dataLoaded)
    if not strdl == "None":
        for topLevel in dataLoaded:
            topLevelContent = getValueArrayParam(dataLoaded, topLevel)
            if topLevel == "on" or topLevel == True: # on
                if isinstance(topLevelContent, list) or isinstance(topLevelContent, dict):
                    for w in topLevelContent:
                        when.append(w)
                else:
                    when.append(topLevelContent)
                    
            if 'jobs' == topLevel and len(topLevelContent)>0:
                for j in topLevelContent:
                    stg = []
                    if len(when)<0:
                        for w in when:
                            stg.append(w)

                    job = CIJob()
                    job.setStage(stg)
                    jobSteps = []
                    jobContent = getValueArrayParam(topLevelContent, j)

                    steps = getValueArrayParam(jobContent, 'steps')
                    if len(steps)>0:
                        if isinstance(steps, list) or isinstance(steps, dict):
                            for step in steps:
                                jobSteps.append(step)
                        else:
                            jobSteps.append(steps)

                    job.setTasks(jobSteps)
                    jobs.append(job)

        if len(when)==0:
            when.append("?")
        
        for job in jobs:
            if len(job.getStage())==0:
                job.setStage(when)
                    
    ciObj = CIObj()
    ciObj.setStages(when)
    ciObj.setJobs(jobs)
    return ciObj

def parseTravisYAML(yamlFile, repoName):
    dataLoaded = loadData(yamlFile,repoName)
    when = []
    jobs = []
    outJob = None
    strdl = str(dataLoaded)
    if not strdl == "None":
        for topLevel in dataLoaded:
            topLevelContent = getValueArrayParam(dataLoaded, topLevel)
            if 'stages' == topLevel:
                if isinstance(topLevelContent, list) or isinstance(topLevelContent, dict):
                    for w in topLevelContent:
                        if isinstance(w, list) or isinstance(w, dict):
                            nameContent = getValueArrayParam(w, "name")
                            if len(str(nameContent))>0:
                                when.append(nameContent)
                            else:
                                when.append(str(w))
                        else:
                            when.append(w)
                else:
                    when.append(topLevelContent)

            if 'jobs' == topLevel:
                includeContent = getValueArrayParam(topLevelContent, 'include')
                for j in includeContent:
                    jobSteps = []
                    jobStages = []

                    stage = getValueArrayParam(j, 'stage')
                    if len(stage)>0:
                        if isinstance(stage, list) or isinstance(stage, dict):
                            for s in stage:
                                jobStages.append(s)
                        else:
                            jobStages.append(stage)

                    install = getValueArrayParam(j, 'install')
                    if len(install)>0:
                        if isinstance(install, list) or isinstance(install, dict):
                            for task in install:
                                jobSteps.append(task)
                        else:
                            jobSteps.append(install)

                        if len(jobStages)==0:
                            jobStages.append("install")
                    
                    script = getValueArrayParam(j, 'script')
                    if len(script)>0:
                        if isinstance(script, list) or isinstance(script, dict):
                            for task in script:
                                jobSteps.append(task)
                        else:
                            jobSteps.append(script)
                        
                        if len(jobStages)==0:
                            jobStages.append("script")

                    '''env = getValueArrayParam(j, 'env')
                    if len(env)>0:
                        if isinstance(env, list) or isinstance(env, dict):
                            for task in env:
                                jobSteps.append(task)
                        else:
                            jobSteps.append(env)
                        
                        if len(jobStages)==0:
                            jobStages.append("env")'''

                    job = CIJob()
                    job.setStage(jobStages)
                    job.setTasks(jobSteps)
                    jobs.append(job)

            elif topLevel in getMainYMLStages():
                when.append(topLevel)
                jobSteps = []
                jobStages = []
                jobStages.append(topLevel)
                outJob = CIJob()
                outJob.setStage(jobStages)

                if isinstance(topLevelContent, list) or isinstance(topLevelContent, dict):
                    for tlc in topLevelContent:
                        jobSteps.append(tlc)
                else:
                    jobSteps.append(topLevelContent)

                jobTasks = outJob.getTasks()
                for step in jobSteps:
                    jobTasks.append(step)
                outJob.setTasks(jobTasks)
                jobs.append(outJob)

        if len(when)==0:
            when.append("?")
            
    ciObj = CIObj()
    ciObj.setStages(when)
    ciObj.setJobs(jobs)
    return ciObj

def loadData(ymlFile, repoName):
    try:
        dataLoaded = yaml.safe_load(open(ymlFile))
        return dataLoaded
    except Exception as e:
        aux.writeInLogFile("> [EXCEPT] Repositorio '" + repoName + "': el fichero de configuración " + str(ymlFile) + " no se ha podido parsear" + "; [" + str(e) + "]")
        return None
    
def getDataYAML(yamlContent):
    # Write YAML file
    with io.open('data.yaml', 'w', encoding='utf8') as outfile:
        yaml.dump(yamlContent, outfile, default_flow_style=False, allow_unicode=True)
        
    # Read YAML file
    with open("data.yaml", 'r') as stream:
        dataLoaded = yaml.safe_load(stream)
        
    return dataLoaded

def getValueArrayParam(level,param):
    try:
        value = level[param]
    except:
        value = ""
    return value

def getMainYMLStages():
    stages = []
    stages.append('before_install')
    stages.append('install')
    stages.append('after_install')
    stages.append('before_script')
    stages.append('script')
    stages.append('after_script')
    return stages

def parseConfigParam(l1, l2):
    dataLoaded = yaml.safe_load(open("config.yml"))
    l1Content = getValueArrayParam(dataLoaded, l1)
    l2Content = getValueArrayParam(l1Content, l2)
    return l2Content

def makeYMLTmpFile(repo, path, boGitHub):
    decoded = aux.getFileContent(repo, path, boGitHub)

    if isinstance(decoded, list):
        i = 0
        for d in decoded:
            if "yml" in d.getExtension() or "yaml" in d.getExtension():
                parts = aux.getStrToFile(d.getContent())
        
                try:
                    fileName = str(tmpFile + "_" + str(i)) + "." + str(d.getExtension())
                    with open(fileName, 'a') as f:
                        for part in parts:
                            f.write(part + "\n")
                finally:
                    i = i+1
                    f.close()
    else:
        parts = aux.getStrToFile(decoded)
    
        try:
            fileName = tmpFile + ".yml"
            with open(fileName, 'a') as f:
                for part in parts:
                    f.write(part + "\n")
        finally:
            f.close()

def addStringOrList(eToAdd):
    lReturn = []
    if isinstance(eToAdd, list) or isinstance(eToAdd, dict):
        for e in eToAdd:
            lReturn.append(e)
    else:
        lReturn.append(eToAdd)
    
    return lReturn

boPrintCIObjs = True
config = "process"
tmpDirectory = parseConfigParam(config, "tmpDirectory")
tmpFile = tmpDirectory + parseConfigParam(config, "tmpFile")