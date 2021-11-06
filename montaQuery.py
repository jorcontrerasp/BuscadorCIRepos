class MontaQuery():
    language = ""
    stars = ">=9000"
    forks = ">=600"
    created = ">2016-01-01"
    pushed = ">2021-01-01"
    archived = "false"
    qIs = "public"

    def __init__(self):
        print("INIT - MontaQuery.py")

    def getQueryIni(self):
        queryIni = ""

        if len(self.created)>0:
            queryIni += " created:" + self.created

        if len(self.pushed)>0:
            queryIni += " pushed:" + self.pushed

        if len(self.stars)>0:
            queryIni += " stars:" + self.stars

        if len(self.forks)>0:
            queryIni += " forks:" + self.forks

        if len(self.language)>0:
            queryIni += " language:" + self.language

        if len(self.archived)>0:
            queryIni += " archived:" + self.archived

        if len(self.qIs)>0:
            queryIni += " is:" + self.qIs

        return queryIni

mQuery = MontaQuery()