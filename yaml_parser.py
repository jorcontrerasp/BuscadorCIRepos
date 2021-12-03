import io
import yaml
import aux_functions as aux

data = yaml.safe_load(open('yml_example_files/defaults.yaml'))
url = data['url']


data2 = yaml.safe_load(open('gitlabCI_yml_example_files/.gitlab-ci.yml'))
stages = data2['stages']
job1 = data2['test-code-job2']
job1_script = job1['script']
#for s in job1_script:
#    print(s)

data3 = yaml.safe_load(open('gitlabCI_yml_example_files/apple_turicreate_gitlab-ci.yml'))
#print(data3)

def parseGitLabYAML(yamlFile):
    #dataLoaded = getDataYAML(yamlFile)
    dataLoaded = yaml.safe_load(open(yamlFile))
    stages = dataLoaded['stages']
    jobs = []
    for topLevel in dataLoaded:

        topLevelContent = dataLoaded[topLevel]
        stage = getValueArrayParam(topLevelContent, 'stage')
        script = getValueArrayParam(topLevelContent, 'script')

        if len(script)>0:
            job = CIJob()
            job.setStage(stage)
            jobTasks = []
            for task in script:
                jobTasks.append(task)
            job.setTasks(jobTasks)
            jobs.append(job)
    ciObj = CIObj()
    ciObj.setStages(stages)
    ciObj.setSJobs(jobs)
    return ciObj
    
def parseGitHubActionsYAML(yamlFile):
    #dataLoaded = getDataYAML(yamlFile)
    # La etiqueta 'on' la detecta como True ¿?
    dataLoaded = yaml.safe_load(open(yamlFile))
    jobs = []
    when = []
    for topLevel in dataLoaded:
        topLevelContent = dataLoaded[topLevel]
        if topLevel == True: # on
            for w in topLevelContent:
                when.append(w)
        if 'jobs' == topLevel and len(topLevelContent)>0:
            for j in topLevelContent:
                job = CIJob()
                job.setStage(when)
                jobSteps = []
                jobContent = topLevelContent[j]
                steps = getValueArrayParam(jobContent, 'steps')
                if len(steps)>0:
                    for step in steps:
                        jobSteps.append(step)
                job.setTasks(jobSteps)
                jobs.append(job)
                    
    ciObj = CIObj()
    ciObj.setStages(when)
    ciObj.setSJobs(jobs)
    return ciObj
    
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

class CIJob:
    stage = ""
    tasks = [] 

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
    stages = []
    jobs = []

    # GETTER & SETTER
    def getStages(self):
        return self.stages

    def setStages(self, stages):
        self.stages = stages

    def getJobs(self):
        return self.jobs

    def setSJobs(self, jobs):
        self.jobs = jobs



f = "gitlabCI_yml_example_files/apple_turicreate_gitlab-ci.yml"
obj = parseGitLabYAML(f)

f = "githubActions_yml_example_files/hacker-laws_build-on-pull-request.yaml"
obj = parseGitHubActionsYAML(f)

print("Parseo finalizado.")