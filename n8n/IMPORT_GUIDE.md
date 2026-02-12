# Guia de Importação - Workflows IAudit no n8n

## 📋 Pré-requisitos

1. **n8n rodando**: Acesse http://localhost:5678
2. **Credenciais configuradas**:
   - Supabase (PostgreSQL)
   - InfoSimples API Token

---

## 🔧 Passo 1: Configurar Credenciais

### Supabase (PostgreSQL)

1. No n8n, vá em **Settings** → **Credentials** → **New**
2. Selecione **Postgres**
3. Preencha:
   - **Name**: `Supabase IAudit`
   - **Host**: `db.XXXXX.supabase.co` (do seu projeto)
   - **Database**: `postgres`
   - **User**: `postgres`
   - **Password**: (senha do projeto)
   - **Port**: `5432`
   - **SSL**: Ativado
4. Clique em **Save**

### InfoSimples API (Opcional - já está hardcoded nos workflows)

Token já configurado: `sntc-QB4cRyQ19y-VgLlBZSwh_41YupJFE9g_-Ye`

---

## 📥 Passo 2: Importar Workflows

### Método 1: Via Interface (Recomendado)

1. Acesse http://localhost:5678
2. Clique em **Workflows** → **Add Workflow** → **Import from File**
3. Selecione os arquivos na pasta `IAudit/n8n/workflows/`:
   - `Agendador_IAudit.json`
   - `Consulta_CND_Federal.json`
   - `Consulta_CND_PR.json` (se criado)
   - `Consulta_FGTS.json` (se criado)

### Método 2: Via API (Avançado)

```bash
curl -X POST http://localhost:5678/rest/workflows \\
  -H "Content-Type: application/json" \\
  -d @IAudit/n8n/workflows/Agendador_IAudit.json
```

---

## ✅ Passo 3: Ativar Workflows

1. Abra cada workflow importado
2. Clique no botão **Active** (canto superior direito)
3. Verifique se o status mudou para "Active" (verde)

---

## 🧪 Passo 4: Testar

### Teste Manual do Agendador

1. Abra o workflow **Agendador_IAudit**
2. Clique em **Execute Workflow** (botão de play)
3. Verifique os logs de execução

### Teste do Webhook CND Federal

```bash
curl -X POST http://localhost:5678/webhook/consulta-cnd-federal \\
  -H "Content-Type: application/json" \\
  -d '{
    "consulta_id": "uuid-teste",
    "cnpj": "00000000000191"
  }'
```

---

## 🎨 Personalização (Estilo MonitorHub)

Os workflows já seguem a arquitetura do MonitorHub:

- **Vigilância 24h**: Agendador roda a cada 5 minutos
- **Busca Automática**: CNDs e FGTS consultados automaticamente
- **Rate Limiting**: 1 consulta a cada 3 segundos (configurar no Agendador)
- **Retry Automático**: 3 tentativas com intervalo de 5 minutos

---

## 📊 Monitoramento

Acesse **Executions** no n8n para ver:
- Histórico de execuções
- Erros e sucessos
- Tempo de processamento

---

## ⚠️ Troubleshooting

### Erro: "Credential not found"
- Verifique se criou a credencial `Supabase IAudit`
- Edite o workflow e reselecione a credencial nos nós Postgres

### Erro: "Table does not exist"
- Execute o script `IAudit/database/schema.sql` no Supabase
- Verifique a conexão com o banco

### Webhook não responde
- Verifique se o workflow está **Active**
- Teste a URL: http://localhost:5678/webhook-test/consulta-cnd-federal
