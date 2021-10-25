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

def getFicherosBusquedaCI(herramientaCI):
    ficheros = []
    if herramientaCI in HerramientasCI.CI1.value:
        ficheros.append("Jenkinsfile")
    elif herramientaCI in HerramientasCI.CI2.value:
        ficheros.append(".travis-ci.yml")
        ficheros.append(".travis.yml")
    elif herramientaCI in HerramientasCI.CI3.value:
        ficheros.append(".circleci/config.yml")
        ficheros.append(".circle-ci")
    elif herramientaCI in HerramientasCI.CI4.value:
        ficheros.append(".github/workflows/**.yml")
        ficheros.append(".github/workflows/**.yaml")
    elif herramientaCI in HerramientasCI.CI5.value:
        ficheros.append(".azure-pipelines/pipelines.yml")
        ficheros.append("azure-pipelines.yml")
    elif herramientaCI in HerramientasCI.CI6.value:
        ficheros.append("bamboo-specs/bamboo.yml")
        ficheros.append("bamboo-specs/bamboo.yaml")
    elif herramientaCI in HerramientasCI.CI7.value:
        ficheros.append("NO ME QUEDA CLARO")
    elif herramientaCI in HerramientasCI.CI8.value:
        # ESTE IGUAL HAY QUE BUSCARLO EN EL REPO ENTERO, PUEDE ESTAR EN CUALQUIER RUTA.
        ficheros.append(".gitlab-ci.yml")
    elif herramientaCI in HerramientasCI.CI9.value:
        ficheros.append("codeship-services.yml")
        ficheros.append("codeship-steps.yml")
        ficheros.append("codeship-steps.json")
    elif herramientaCI in HerramientasCI.CI10.value:
        ficheros.append(".teamcity/settings.kts")
    elif herramientaCI in HerramientasCI.CI11.value:
        ficheros.append(".bazelci/presubmit.yml")
        ficheros.append(".bazelci/build_bazel_binaries.yml")
        ficheros.append(".bazelrc")
    elif herramientaCI in HerramientasCI.CI2.value:
        ficheros.append(".semaphore/semaphore.yml")
        ficheros.append(".semaphoreci")
    elif herramientaCI in HerramientasCI.CI3.value:
        ficheros.append("Appveyor.yml")

    return ficheros