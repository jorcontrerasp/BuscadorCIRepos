var = ".circleci/config.yml"
var1 = var.split("/")
print(var)
print(len(var1))
print(var1[0])
print(var1[1])
var2 = '/'.join(var1)
print(var2)