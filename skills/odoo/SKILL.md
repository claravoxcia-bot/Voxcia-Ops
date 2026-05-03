---
name: odoo
description: Procedimentos padrão para lançamento de faturas/contas a pagar, fornecedores, anexos PDF e rotinas financeiras no Odoo. Use quando for necessário: criar fornecedor, lançar fatura de fornecedor, anexar PDF, definir número da NF (l10n_latam_document_number) e postar fatura via JSON-RPC/API.
---

# Skill: Odoo — Procedimentos padrão

Breve: esta skill contém o fluxo mínimo e recursos reutilizáveis para inserir faturas de fornecedor no Odoo conforme nossas práticas (fornecedor -> contas -> carregar). Carregue as referências apenas quando precisar executar a tarefa.

Triggers (quando usar esta skill):
- "inserir fatura", "criar fatura fornecedor", "anexar PDF Odoo", "contas a pagar" e consultas similares sobre lançamentos no Odoo.

Resumo do fluxo (baixo esforço / alto confiança):
1. Verificar/obter credenciais JSON-RPC: (db, login, password/token).
2. Procurar parceiro por CNPJ (campo vat). Se não existir, criar res.partner com supplier_rank=1.
3. Determinar journal (diário) e account.account (conta contábil) — usar código contábil quando possível.
4. Criar account.move com:
   - move_type: in_invoice
   - partner_id
   - invoice_date / invoice_date_due
   - journal_id
   - invoice_line_ids: [(0,0,{'name', 'quantity', 'price_unit', 'account_id'})]
   - invoice_origin / ref = número da NF (quando aplicável)
5. Definir número da NF: escrever l10n_latam_document_number = <número> e l10n_latam_manual_document_number = True.
6. Anexar PDF via ir.attachment (datas = base64 do arquivo, res_model='account.move', res_id=<id>).
7. action_post() para validar/postar — atenção a validações locais (ex.: exigir número do documento, sequências, series).

Práticas recomendadas / nota operacional:
- Sempre usar account_id por código (ex.: 3.01.01.03.01.01) para evitar validações de conta vazia.
- Anexar o PDF antes de postar quando o módulo documentos/account_invoice_extract estiver ativo.
- Quando o Odoo reclamar do número do documento, definir l10n_latam_document_number e ref e reenviar action_post.

Recursos incluídos (referências e scripts):
- references/procedures.md — passos detalhados e exemplos (carregado sob demanda).
- scripts/generate_import_csv.py — utilitário para gerar CSV de importação para lançamentos.

Como estender esta skill:
- Editar references/ com novos exemplos (fornecedores, códigos contábeis, diários preferidos).
- Atualizar scripts/ com rotinas que automatizem geração de arquivos de importação ou chamadas JSON-RPC.

Se quiser que eu registre este comportamento como padrão (diário, conta e tags), diga quais valores salvar como padrão e eu atualizo references/defaults.md.

