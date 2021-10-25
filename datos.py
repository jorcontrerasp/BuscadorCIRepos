#AQUÍ se definirán las funciones relacionadas con los datos resultantes.

#Importamos las librerías necesarias.
import pandas as pd
import herramientasCI as ci

def generarDataFrame(listaRepositorios):
    repo1 = listaRepositorios[0]
    df = pd.DataFrame([],
                      index=[repo1.full_name],
                      columns=["GitHub_URL", "Lenguaje"
                               ,ci.HerramientasCI.CI1.value
                               ])
    df.at[repo1.full_name, "GitHub_URL"] = repo1.html_url
    df.at[repo1.full_name, "Lenguaje"] = repo1.language
    df.at[repo1.full_name, ci.HerramientasCI.CI1.value] = " "

    for repo in listaRepositorios[1:len(listaRepositorios)]:
        df2 = pd.DataFrame([],
                          index=[repo.full_name],
                          columns=["GitHub_URL", "Lenguaje"
                                   ,ci.HerramientasCI.CI1.value
                                   ])
        df2.at[repo.full_name, "GitHub_URL"] = repo.html_url
        df2.at[repo.full_name, "Lenguaje"] = repo.language
        df2.at[repo.full_name, ci.HerramientasCI.CI1.value] = " "
        df = df.append(df2)

    return df

def generarEXCEL(df, pFichero):
    print("Generando fichero Excel...")
    df.to_excel(pFichero + ".xlsx")

def generarCSV(df, pFichero):
    print("Generando fichero Csv...")
    df.to_csv(pFichero + ".csv")