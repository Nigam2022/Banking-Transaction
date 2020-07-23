import pandas as pd
import random as rnd
import csv
import shutil
from tempfile import NamedTemporaryFile

def getDeno(x) :
  ret = {1000 : 0, 500 : 0, 10 : 0}
  if x >= 1000 :
    ret[1000] = x // 1000
    x %= 1000
  if x >= 500 :
    ret[500] = x // 500
    x %= 500
  if x >= 10 :
    ret[10] = x // 10
    x %= 10
  return ret


card = set()
acc = set()
bal = set()
atype = list()
pwd = set()

while len(card) != 10 :
    val = rnd.randint(1, 1000000000000000)
    val = "{:016d}".format(val)
    card.add(val)

while len(acc) != 10 :
    val = rnd.randint(1, 1000000000)
    val = "{:010d}".format(val)
    acc.add(val)

while len(bal) != 10 :
    val = rnd.randint(1, 1000000)
    bal.add(str(val))

while len(atype) != 10 :
    val = rnd.randint(1, 2)
    atype.append(val)

while len(pwd) != 10 :
    val = rnd.randint(1, 1000)
    val = "{:4d}".format(val)
    pwd.add(val)

card = list(card)
acc = list(acc)
bal = list(bal)
pwd = list(pwd)

dataDict = {'CardNumber' : card, 'AccountNumber' : acc, 'Balance' : bal, 'AccountType' : atype, 'Password' : pwd}
df = pd.DataFrame(dataDict)
df.to_csv('AccountDetails.csv', index = False)         # Save CSV of AccountDetails



data = pd.read_csv('AccountDetails.csv')
amount = list(data.Balance)
account = list(data.AccountNumber)
denom_10 = list()
denom_500 = list()
denom_1000 = list()

for x in amount :
  res = getDeno(x)
  denom_10.append(res[10])
  denom_500.append(res[500])
  denom_1000.append(res[1000])

dataDict = {'Account' : account, '10' : denom_10, '500' : denom_500, '1000' :denom_1000}
df = pd.DataFrame(dataDict)
df.to_csv('AtmDetails.csv', index = False)
