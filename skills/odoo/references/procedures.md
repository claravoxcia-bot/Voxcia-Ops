# Procedimentos detalhados — Skill Odoo

1) Autenticação (JSON-RPC):
   - Endpoint: <odoo_base>/jsonrpc
   - Chamada: service='common', method='login', args=[db, login, password]

2) Criar/usar parceiro (res.partner):
   - Buscar por vat (CNPJ). Ex.: search_read(['vat','=', '40432544000147'])
   - Se não existir: create({'name': nome, 'vat': cnpj, 'supplier_rank': 1})

3) Criar fatura de fornecedor (account.move):
   - Campos mínimos:
     * move_type: 'in_invoice'
     * partner_id
     * invoice_date / invoice_date_due (YYYY-MM-DD)
     * journal_id (id do diário)
     * invoice_line_ids: [(0,0,{'name','quantity',1,'price_unit',valor,'account_id',account_id})]
   - Após criação, definir número da NF (se aplicável):
     * write({'l10n_latam_document_number': '27559080', 'l10n_latam_manual_document_number': True, 'ref': '27559080'})
   - Para postar: action_post([id]) — trate erros de validação e preencha campos obrigatórios.

4) Anexar PDF:
   - Criar ir.attachment com campos: name, type='binary', datas=<base64>, res_model='account.move', res_id=<id>, mimetype='application/pdf'

5) Exceções comuns e como resolvê-las:
   - Missing required account on accountable line: fornecer account_id correto na invoice_line.
   - Defina o número do documento nas seguintes faturas: preencher l10n_latam_document_number + ref.
   - Sequências/series: quando houver regra fiscal, informe série/número ou peça ao usuário.

6) Metadados padrão que podemos salvar em references/defaults.md:
   - journal_default: id ou nome (ex.: Purchases)
   - account_default: código contábil preferido
   - user_default: email do responsável

