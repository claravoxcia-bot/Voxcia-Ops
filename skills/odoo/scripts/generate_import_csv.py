#!/usr/bin/env python3
"""Gerador simples de CSV para importação de faturas (account.move) no Odoo.
Gera colunas básicas: move_type,partner,invoice_date,invoice_date_due,journal,invoice_line_name,invoice_line_account_code,invoice_line_price_unit,ref
Uso: python3 generate_import_csv.py --out vendas.csv --partner "CLARO S.A." --cnpj 40432544000147 --date 2026-05-03 --journal Purchases --account 3.01.01.03.01.01 --amount 35.00 --nf 27559080
"""
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--partner', required=True)
parser.add_argument('--cnpj', required=False)
parser.add_argument('--date', required=True)
parser.add_argument('--journal', required=True)
parser.add_argument('--account', required=True)
parser.add_argument('--amount', required=True)
parser.add_argument('--nf', required=False)
args = parser.parse_args()

headers = ['move_type','partner','invoice_date','invoice_date_due','journal','invoice_line_name','invoice_line_account_code','invoice_line_price_unit','ref']
rows = []
rows.append(['in_invoice', args.partner, args.date, args.date, args.journal, f'Invoice {args.nf or ""}', args.account, args.amount, args.nf or ''])

with open(args.out, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(headers)
    w.writerows(rows)

print('CSV gerado em', args.out)

