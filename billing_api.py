import csv

billings = {}
num_of_printers = {}

with open('billings.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        breakpoint()
        client = row['CustomerId']
        if client not in billings:
            billings[client] = dict.fromkeys(['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'],0)
            num_of_printers[client] = 1
        else:
            num_of_printers[client] += 1
