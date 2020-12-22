# BillingAPI

Sistema de faturamento para uma empresa de aluguel de impressoras 3D.


A aplicação recebe via linha de comando o mês da cobrança (abreviado) e o
caminho para um arquivo .csv contendo o registro de todos os consumos para faturamento.
São impressos na tela o nome do cliente e o valor total da cobrança para o mês desejado.


**Execução**
> python billing.py `mes_desejado` `consumo_impressoras.csv`


**Exemplo de Execução**
> python billing.py `mar` `consumo_impressoras.csv`


`Cliente 1: $107.26
 Cliente 2: $11.61
 Cliente 3: $0.00`

