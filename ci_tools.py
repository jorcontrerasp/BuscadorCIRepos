#AQUÍ se definirán las herramientas CI del experimento.

#Importamos las librerías necesarias.
from enum import Enum

class HerramientasCI(Enum):
    CI1 = "Jenkins"
    CI2 = "Travis"
    CI3 = "Circle CI"
    CI4 = "GitHub Actions"
    CI5 = "Azure Pipelines"
    CI6 = "Bamboo"
    CI7 = "Concourse"
    CI8 = "GitLab CI"
    CI9 = "Codeship"
    CI10 = "TeamCity"
    CI11 = "Bazel"
    CI12 = "Semaphore CI"
    CI13 = "AppVeyor"

def getCIToolsValueList():
    lCITools = []
    lCITools.append(HerramientasCI.CI1.value)
    lCITools.append(HerramientasCI.CI2.value)
    lCITools.append(HerramientasCI.CI3.value)
    lCITools.append(HerramientasCI.CI4.value)
    lCITools.append(HerramientasCI.CI5.value)
    lCITools.append(HerramientasCI.CI6.value)
    lCITools.append(HerramientasCI.CI7.value)
    lCITools.append(HerramientasCI.CI8.value)
    lCITools.append(HerramientasCI.CI9.value)
    lCITools.append(HerramientasCI.CI10.value)
    lCITools.append(HerramientasCI.CI11.value)
    lCITools.append(HerramientasCI.CI12.value)
    lCITools.append(HerramientasCI.CI13.value)
    
    return lCITools


def getCISearchFiles(CITool):
    files = []
    if CITool in HerramientasCI.CI1.value:
        files.append("Jenkinsfile")
    elif CITool in HerramientasCI.CI2.value:
        files.append(".travis-ci.yml")
        files.append(".travis.yml")
    elif CITool in HerramientasCI.CI3.value:
        files.append(".circleci/config.yml")
        files.append(".circle-ci")
    elif CITool in HerramientasCI.CI4.value:
        files.append(".github/workflows") #**.yml o **.yaml
    elif CITool in HerramientasCI.CI5.value:
        files.append(".azure-pipelines/pipelines.yml")
        files.append("azure-pipelines.yml")
    elif CITool in HerramientasCI.CI6.value:
        files.append("bamboo-specs/bamboo.yml")
        files.append("bamboo-specs/bamboo.yaml")
    #elif herramientaCI in HerramientasCI.CI7.value:
        # NO ME QUEDA CLARO QUÉ AÑADIR EN ESTE CASO.
    elif CITool in HerramientasCI.CI8.value:
        files.append(".gitlab-ci.yml")
    elif CITool in HerramientasCI.CI9.value:
        files.append("codeship-services.yml")
        files.append("codeship-steps.yml")
        files.append("codeship-steps.json")
    elif CITool in HerramientasCI.CI10.value:
        files.append(".teamcity/settings.kts")
    elif CITool in HerramientasCI.CI11.value:
        files.append(".bazelci/presubmit.yml")
        files.append(".bazelci/build_bazel_binaries.yml")
        files.append(".bazelrc")
    elif CITool in HerramientasCI.CI2.value:
        files.append(".semaphore/semaphore.yml")
        files.append(".semaphoreci")
    elif CITool in HerramientasCI.CI3.value:
        files.append("Appveyor.yml")

    return files