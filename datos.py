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
    df.at[repo1.full_name, "GitHub_URL"] = repo1.html_url
    df.at[repo1.full_name, "Lenguaje"] = repo1.language
    df.at[repo1.full_name, ci.HerramientasCI.CI1.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI2.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI3.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI4.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI5.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI6.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI7.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI8.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI9.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI10.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI11.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI12.value] = " "
    df.at[repo1.full_name, ci.HerramientasCI.CI13.value] = " "

    for repo in listaRepositorios[1:len(listaRepositorios)]:
        df2 = pd.DataFrame([],
                          index=[repo.full_name],
                          columns=["GitHub_URL", "Lenguaje"
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
        df2.at[repo.full_name, "GitHub_URL"] = repo.html_url
        df2.at[repo.full_name, "Lenguaje"] = repo.language
        df2.at[repo.full_name, ci.HerramientasCI.CI1.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI2.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI3.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI4.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI5.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI6.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI7.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI8.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI9.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI10.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI11.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI12.value] = " "
        df2.at[repo.full_name, ci.HerramientasCI.CI13.value] = " "
        df = df.append(df2)

    return df

def generarEXCEL(df, pFichero):
    print("Generando fichero Excel...")
    df.to_excel(pFichero + ".xlsx")

def generarCSV(df, pFichero):
    print("Generando fichero Csv...")
    df.to_csv(pFichero + ".csv")