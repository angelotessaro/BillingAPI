import sys
import csv
import datetime
from calendar import monthrange
import heapq

alugueis = {}
billings = {}
meses = {'1': 'jan', '2': 'fev', 
         '3': 'mar', '4': 'abr',
         '5': 'mai', '6': 'jun',
         '7': 'jul', '8': 'ago',
         '9': 'set', '10': 'out',
         '11': 'nov', '12': 'dez' 
        }

with open(sys.argv[2]) as csv_file:

    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        client = row['CustomerId']
        data_inicio = datetime.datetime.strptime(row['ActivatedAt'], '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(row['DeactivatedAt'], '%Y-%m-%d').date()
        intervalo = [data_inicio, data_fim]
        if client not in alugueis:
            alugueis[client] = [intervalo]
        else:
            alugueis[client].append(intervalo)

    for client in alugueis:
        alugueis[client].sort(key=lambda x:x[0])


    print(alugueis)
    for client in alugueis:
        em_uso = []
        # for intervalo in alugueis[client]:
        #     heapq.heappush(em_uso, intervalo[1])
        for intervalo in alugueis[client]:
            heapq.heappush(em_uso, intervalo[1])
            if intervalo[0] >= em_uso[0]:
                heapq.heappop(em_uso)
            num_meses = intervalo[1].month - intervalo[0].month
            data_inicio = intervalo[0]
            data_fim = intervalo[1]
            for _ in range(num_meses+1):
                if client not in billings:
                    billings[client] = dict.fromkeys(meses.values(),0)
                if data_fim.month == data_inicio.month:
                    mes_billing = meses[str(data_fim.month)]
                    num_of_days = (data_fim - data_inicio).days
                else:
                    mes_billing = data_inicio.month
                    ano_billing = data_inicio.year
                    dias_no_mes = monthrange(ano_billing, mes_billing)[1]
                    num_of_days = dias_no_mes - data_inicio.day + 1
                    mes_billing = meses[str(mes_billing)]
                num_of_printers = len(em_uso)
                if num_of_printers <= 2:
                    valor_cobrado = num_of_days*30/dias_no_mes
                elif num_of_printers >= 6:
                    valor_cobrado = num_of_days*25/dias_no_mes
                else:
                    valor_cobrado = num_of_days*28/dias_no_mes
                billings[client][mes_billing] += valor_cobrado
                if data_inicio.month != 12:
                    data_inicio = data_inicio.replace(day=1,month=data_inicio.month+1)

    breakpoint()

    # mes_ref = sys.argv[1]
    # for client in alugueis:
    #     if num_of_printers[client] <= 2:
            
    #     elif num_of_printers[client] >= 6:


    #     else:
    #     billings[client][mes_ref]
    # print(billings)
            



