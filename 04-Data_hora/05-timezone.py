import pytz
from datetime import datetime

data = datetime.now(pytz.timezone('Europe/Oslo'))
data1 = datetime.now(pytz.timezone('America/Sao_Paulo'))

print(data)
print(data1)
