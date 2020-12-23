import sys
import csv
import datetime
from calendar import monthrange
import heapq

def leitura_arquivo(caminho_arquivo):
    '''
        Realiza a leitura do arquivo .csv com os registros de faturamento

        Args:
            caminho_arquivo(str): Caminho para o arquivo ou apenas o nome caso esteja na mesma pasta

        Return:
            alugueis(dict): Dicionário com os dados para cada cliente
    '''

    with open(caminho_arquivo) as csv_file:
        alugueis = {}
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
    return alugueis

def remove_overlap(intervals):
    for i in intervals:
        for j in intervals:
            if i != j:
                if i[0] == j[0] and i[1] > j[1]:
                    right_interval = [j[1], i[1]]
                    intervals.remove(i)
                    i = j
                    intervals.append(i)
                    intervals.append(right_interval)
                elif i[0] < j[0] and i[1] == j[1]:
                    left_interval = [i[0], j[0]]
                    intervals.remove(i)
                    i = j
                    intervals.append(i)
                    intervals.append(left_interval)
                elif i[0] < j[0] and i[1] > j[1]:
                    left_interval = [i[0], j[0]]
                    right_interval = [j[1], i[1]]
                    intervals.remove(i)
                    i = j
                    intervals.append(i)
                    intervals.append(left_interval)
                    intervals.append(right_interval)
    return intervals

def main():

    #Leitura do Arquivo
    alugueis = leitura_arquivo(sys.argv[2])
    billings = {}
    meses = {'1': 'jan', '2': 'fev',
            '3': 'mar', '4': 'abr',
            '5': 'mai', '6': 'jun',
            '7': 'jul', '8': 'ago',
            '9': 'set', '10': 'out',
            '11': 'nov', '12': 'dez'
            }

    for client in alugueis:
        alugueis[client] = remove_overlap(alugueis[client])

    # Lista com todas as datas de início dos alugueis para cada cliente
    todos_ativacao = {}
    for client in alugueis:
        # Ordena os alugueis de cada cliente pela data de início
        alugueis[client].sort(key=lambda x:x[0])
        for intervalo in alugueis[client]:
            if client not in todos_ativacao:
                todos_ativacao[client] = []
            todos_ativacao[client].append(intervalo[0])

    for client in alugueis:
        # Heap queue dos alugueis correntes
        em_uso = []
        for intervalo in alugueis[client]:
            while intervalo[0] in todos_ativacao[client]:
                todos_ativacao[client].remove(intervalo[0])
                heapq.heappush(em_uso, intervalo[1])
            while intervalo[0] >= em_uso[0]:
                heapq.heappop(em_uso)
            num_meses = intervalo[1].month - intervalo[0].month
            data_inicio = intervalo[0]
            data_fim = intervalo[1]

            for _ in range(num_meses+1):
                if client not in billings:
                    billings[client] = dict.fromkeys(meses.values(),0)
                if data_fim.month == data_inicio.month:
                    dias_no_mes = monthrange(ano_billing, data_fim.month)[1]
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

    # Impressão dos resultados
    mes_ref = sys.argv[1]
    for client in billings:
        print('Cliente %s: $%.2f' %(client, billings[client][mes_ref]))

if __name__ == '__main__':
    main()
