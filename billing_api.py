import csv
import datetime
from calendar import monthrange

billings = {}
num_of_printers = {}
meses = {'1': 'jan', '2': 'fev', 
         '3': 'mar', '4': 'abr',
         '5': 'mai', '6': 'jun',
         '7': 'jul', '8': 'ago',
         '9': 'set', '10': 'out',
         '11': 'nov', '12': 'dez' 
        }

with open('billings.csv') as csv_file:

    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        client = row['CustomerId']
        data_inicio = datetime.datetime.strptime(row['ActivatedAt'], '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(row['DeactivatedAt'], '%Y-%m-%d').date()

        if client not in billings:
            billings[client] = dict.fromkeys(meses.values(),0)
            num_of_printers[client] = 1
        else:
            num_of_printers[client] += 1

        num_meses = data_fim.month - data_inicio.month
        for _ in range(num_meses+1):
            if data_fim.month == data_inicio.month:
                mes_billing = meses[str(data_fim.month)]
                num_of_days = (data_fim - data_inicio).days
                billings[client][mes_billing] += num_of_days
                break
            else:
                mes_billing = data_inicio.month
                ano_billing = data_inicio.year
                ultimo_dia = monthrange(ano_billing, mes_billing)[1]
                num_of_days = ultimo_dia - data_inicio.day
                mes_billing = meses[str(mes_billing)]
                billings[client][mes_billing] += num_of_days
                data_inicio = data_inicio.replace(day=1,month=data_inicio.month+1)
    print(billings)
            



