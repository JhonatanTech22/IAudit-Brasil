# Guia de Instalação e Teste do n8n para IAudit

## 🚀 Opção 1: Instalar n8n Localmente (Recomendado)

### Passo 1: Habilitar Scripts no PowerShell

Abra o PowerShell **como Administrador** e execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Passo 2: Instalar n8n

```powershell
npm install -g n8n
```

### Passo 3: Iniciar n8n

```powershell
n8n start
```

O n8n estará disponível em: **http://localhost:5678**

---

## 📥 Opção 2: Importar Workflows no n8n

### 1. Acessar Interface

Abra o navegador em: http://localhost:5678

### 2. Criar Conta

Na primeira vez, crie uma conta local (dados ficam apenas no seu computador)

### 3. Importar Workflows

Para cada arquivo em `IAudit/n8n/workflows/`:

1. Clique em **"+"** (novo workflow)
2. Clique nos **3 pontos** (menu) → **Import from File**
3. Selecione o arquivo JSON:
   - `Agendador_IAudit.json`
   - `Consulta_CND_Federal.json`
   - `Consulta_CND_PR.json`
   - `Consulta_FGTS.json`

### 4. Configurar Credenciais (Opcional para Teste)

Os workflows já têm o token da InfoSimples hardcoded, mas para produção você precisaria:

**Supabase (PostgreSQL):**
- Settings → Credentials → New → Postgres
- Nome: `Supabase IAudit`
- Host: `db.xxxxx.supabase.co`
- Database: `postgres`
- User: `postgres`
- Password: (sua senha)
- Port: `5432`
- SSL: ✅ Ativado

### 5. Ativar Workflows

Para cada workflow importado:
1. Abra o workflow
2. Clique em **"Active"** (toggle no canto superior direito)
3. Verifique se ficou verde

---

## 🧪 Opção 3: Testar com Servidor Mock (Sem n8n)

Criei um servidor Python que simula os workflows do n8n para você testar sem precisar instalar nada.

### Executar o Servidor Mock

```powershell
cd "c:\Users\Micro\Desktop\alan turing 10.02.2026\IAudit"
python mock_n8n_server.py
```

O servidor estará em: **http://localhost:5678**

### Endpoints Disponíveis

1. **Dashboard**: http://localhost:5678/
2. **Webhook CND Federal**: http://localhost:5678/webhook/consulta-cnd-federal
3. **Webhook CND PR**: http://localhost:5678/webhook/consulta-cnd-pr
4. **Webhook FGTS**: http://localhost:5678/webhook/consulta-fgts
5. **Agendador**: http://localhost:5678/webhook/agendador

### Testar via Browser ou cURL

**No navegador:**
- Acesse http://localhost:5678/
- Clique nos botões para testar cada workflow

**Via cURL:**
```powershell
# Testar CND Federal
curl -X POST http://localhost:5678/webhook/consulta-cnd-federal `
  -H "Content-Type: application/json" `
  -d '{\"cnpj\": \"00000000000191\", \"consulta_id\": \"test-123\"}'

# Testar Agendador
curl http://localhost:5678/webhook/agendador
```

---

## 📊 Workflows Disponíveis

### 1. Agendador_IAudit
**Função**: Busca consultas agendadas e dispara execução

**Fluxo:**
1. Busca empresas ativas no banco
2. Verifica se está no horário agendado
3. Cria registros de consulta
4. Dispara workflows específicos (CND Federal, CND PR, FGTS)

**Teste Manual:**
- n8n: Abra o workflow e clique em "Execute Workflow"
- Mock: GET http://localhost:5678/webhook/agendador

### 2. Consulta_CND_Federal
**Função**: Consulta Certidão Negativa Federal via InfoSimples

**Fluxo:**
1. Recebe CNPJ e consulta_id
2. Chama API InfoSimples
3. Salva PDF no Google Drive
4. Atualiza status no banco

**Teste Manual:**
```json
POST http://localhost:5678/webhook/consulta-cnd-federal
{
  "cnpj": "00000000000191",
  "consulta_id": "uuid-teste"
}
```

### 3. Consulta_CND_PR
**Função**: Consulta Certidão Negativa do Paraná

**Fluxo:**
1. Recebe CNPJ e IE_PR
2. Chama API InfoSimples
3. Salva PDF
4. Atualiza banco

**Teste Manual:**
```json
POST http://localhost:5678/webhook/consulta-cnd-pr
{
  "cnpj": "00000000000191",
  "ie_pr": "1234567890",
  "consulta_id": "uuid-teste"
}
```

### 4. Consulta_FGTS
**Função**: Consulta Regularidade do FGTS

**Fluxo:**
1. Recebe CNPJ
2. Chama API InfoSimples
3. Salva PDF
4. Atualiza banco

**Teste Manual:**
```json
POST http://localhost:5678/webhook/consulta-fgts
{
  "cnpj": "00000000000191",
  "consulta_id": "uuid-teste"
}
```

---

## 🔗 URLs de Teste

### Com n8n Real (após instalação)
- Interface: http://localhost:5678
- Webhooks: http://localhost:5678/webhook/[nome-do-webhook]

### Com Servidor Mock (Python)
- Interface: http://localhost:5678
- Webhooks: http://localhost:5678/webhook/[nome-do-webhook]

---

## ✅ Checklist de Verificação

- [ ] n8n instalado e rodando OU servidor mock rodando
- [ ] Workflows importados (se usando n8n real)
- [ ] Workflows ativados (toggle verde)
- [ ] Teste do Agendador executado com sucesso
- [ ] Teste de webhook CND Federal retorna JSON
- [ ] Teste de webhook CND PR retorna JSON
- [ ] Teste de webhook FGTS retorna JSON

---

## 🎯 Próximos Passos

1. **Escolha uma opção**: n8n real ou servidor mock
2. **Execute os testes**: Verifique se os endpoints respondem
3. **Integre com Frontend**: Os botões "Forçar Consulta" podem chamar esses webhooks
4. **Configure Supabase**: Para persistência real dos dados

---

## 💡 Dicas

- **Servidor Mock**: Ideal para desenvolvimento e testes rápidos
- **n8n Real**: Necessário para produção e integração completa
- **Logs**: Verifique o console do servidor para ver as requisições
- **Erros**: Se algo não funcionar, verifique as credenciais e conexões

---

**Escolha a opção que preferir e me avise se precisar de ajuda!**
