from gate_ways.account.secretsManager import SecretRepo

sr =SecretRepo()
print(sr.read("myId2"))