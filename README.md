# IAudit - Sistema de Auditoria Fiscal Automatizada

![IAudit Logo](https://img.shields.io/badge/IAudit-v1.0.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Demo%20Ready-green?style=for-the-badge)

Sistema completo para automação de consultas fiscais com monitoramento contínuo de certidões negativas e regularidade fiscal.

## 📋 Visão Geral

O IAudit é uma solução integrada que combina:
- **Frontend Streamlit**: Interface web moderna e intuitiva
- **Backend n8n**: Workflows de automação para consultas via API
- **Database Supabase**: Armazenamento PostgreSQL com Row Level Security
- **Google Drive**: Armazenamento de PDFs das certidões
- **Notificações**: Alertas automáticos por email

## ✨ Funcionalidades

### 📊 Dashboard Inteligente
- KPIs em tempo real (empresas ativas, consultas, taxa de sucesso, alertas)
- Gráficos interativos de volume de consultas
- Lista de alertas recentes

### 📤 Upload em Lote
- Importação via CSV/XLSX
- Validação automática de CNPJ (formato e dígitos verificadores)
- Detecção de duplicatas
- Configuração de agendamento por lote

### 🏢 Gestão de Empresas
- Listagem com filtros avançados
- Busca por razão social ou CNPJ
- Ações rápidas: visualizar, editar, forçar consulta, pausar
- Status visual com ícones coloridos

### 📋 Detalhes Completos
- Resumo com últimas consultas de cada tipo
- Histórico completo paginado
- Configuração de agendamento individual
- Download de PDFs

### 🔔 Tipos de Consulta
- ✅ **CND Federal**: Certidão Negativa de Débitos Federais
- ✅ **CND Paraná**: Certidão Negativa de Débitos Estaduais (PR)
- ✅ **FGTS**: Certificado de Regularidade do FGTS

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Streamlit     │  Frontend (Python)
│   Frontend      │  - Dashboard, Upload, Empresas, Detalhes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Supabase     │  Database (PostgreSQL)
│    Database     │  - empresas, consultas, logs_execucao
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      n8n        │  Automation Backend
│   Workflows     │  - Agendador, Consultas, Notificações
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ InfoSimples │   │Google Drive │
│     API     │   │   Storage   │
└─────────────┘   └─────────────┘
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- Node.js 16+ (para n8n)
- Conta Supabase
- Conta Google Cloud (para Drive API)
- Token InfoSimples API

### 1. Frontend (Streamlit)

```powershell
cd IAudit/frontend

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Executar aplicação
streamlit run Home.py
```

### 2. Database (Supabase)

1. Criar projeto em [supabase.com](https://supabase.com)
2. Executar script SQL:
   ```sql
   -- Copiar conteúdo de database/schema.sql
   ```
3. Copiar URL e Anon Key para `.env`

### 3. Backend (n8n)

```powershell
# Instalar n8n globalmente
npm install -g n8n

# Executar n8n
n8n start

# Importar workflows de n8n/workflows/
# Configurar credenciais conforme n8n/IMPORT_GUIDE.md
```

## 📝 Configuração

### Variáveis de Ambiente

Criar arquivo `.env` no diretório `frontend/`:

```env
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-anon-key-aqui

# n8n Webhooks (opcional)
N8N_WEBHOOK_FORCE_CONSULTATION=https://n8n.example.com/webhook/force
N8N_WEBHOOK_PAUSE_COMPANY=https://n8n.example.com/webhook/pause
```

### Credenciais n8n

Configurar no painel do n8n:

| Serviço | Credencial | Onde Obter |
|---------|-----------|------------|
| InfoSimples | API Token | [api.infosimples.com](https://api.infosimples.com) |
| Google Drive | Service Account JSON | Google Cloud Console |
| Email (Resend/SES) | API Key | Painel do serviço |
| Supabase | URL + Anon Key | Painel Supabase |

## 📖 Uso

### Upload de Empresas

1. Preparar planilha CSV/XLSX com colunas:
   - `CNPJ` (obrigatório)
   - `Razao Social` (obrigatório)
   - `IE_PR`, `Email`, `WhatsApp` (opcionais)

2. Acessar página **Upload**
3. Fazer upload do arquivo
4. Revisar preview e validações
5. Configurar periodicidade e horário
6. Confirmar cadastro

### Monitoramento

1. Acessar **Dashboard** para visão geral
2. Ver **Empresas** para lista detalhada
3. Clicar em 👁 para ver **Detalhes** de uma empresa
4. Usar filtros para encontrar irregularidades

### Ações Rápidas

- **🔄 Forçar Consulta**: Executar consulta imediatamente
- **⏸ Pausar**: Suspender consultas automáticas
- **✏ Editar**: Alterar configurações
- **📥 Download PDF**: Baixar certidão

## 🎨 Design

O frontend foi desenvolvido com inspiração no **MonitorHub**, utilizando:

- **Cores**: Azul profissional (#1e40af) com gradientes
- **Tipografia**: Inter (Google Fonts)
- **Componentes**: Cards com sombras, ícones de status coloridos
- **Responsividade**: Layout adaptável para diferentes telas
- **Interatividade**: Gráficos Plotly, filtros dinâmicos

## 📁 Estrutura de Pastas

```
IAudit/
├── frontend/
│   ├── Home.py                 # Página inicial
│   ├── pages/
│   │   ├── 00_Dashboard.py     # Dashboard com KPIs
│   │   ├── 01_Upload.py        # Upload de empresas
│   │   ├── 02_Empresas.py      # Lista de empresas
│   │   └── 03_Detalhes.py      # Detalhes da empresa
│   ├── utils/
│   │   ├── validators.py       # Validação de CNPJ
│   │   ├── formatters.py       # Formatação de dados
│   │   ├── mock_data.py        # Dados de demonstração
│   │   └── styles.py           # CSS customizado
│   ├── .streamlit/
│   │   └── config.toml         # Configuração do tema
│   ├── requirements.txt
│   └── .env.example
├── database/
│   └── schema.sql              # Schema PostgreSQL
├── n8n/
│   ├── workflows/              # JSON dos workflows
│   └── IMPORT_GUIDE.md         # Guia de importação
└── README.md
```

## 🧪 Modo Demonstração

O sistema funciona em **modo demonstração** sem credenciais do Supabase:

- Dados mock realistas
- Todas as funcionalidades visuais
- Validações funcionais
- Simulação de ações

Para produção, configure as credenciais no `.env`.

## 🔒 Segurança

- **RLS (Row Level Security)** no Supabase
- **Validação de CNPJ** com dígitos verificadores
- **Sanitização de inputs**
- **HTTPS obrigatório** em produção

## 📊 Workflows n8n

### 1. Agendador_IAudit
Executa periodicamente para buscar consultas agendadas.

### 2. Consulta_CND_Federal
Consulta certidão federal via InfoSimples API.

### 3. Consulta_CND_PR
Consulta certidão estadual do Paraná.

### 4. Consulta_FGTS
Consulta regularidade do FGTS.

### 5. Notificador_Alertas
Envia emails quando detecta irregularidades.

## 🐛 Troubleshooting

### Frontend não inicia
```powershell
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de conexão Supabase
- Verificar URL e Anon Key no `.env`
- Confirmar que o projeto Supabase está ativo

### n8n workflows não executam
- Verificar credenciais configuradas
- Testar manualmente cada workflow
- Checar logs do n8n

## 📞 Suporte

- **Documentação InfoSimples**: https://api.infosimples.com
- **Docs Supabase**: https://supabase.com/docs
- **Community n8n**: https://community.n8n.io
- **Streamlit Docs**: https://docs.streamlit.io

## 📄 Licença

Este projeto é proprietário. Todos os direitos reservados.

## 👥 Autores

Desenvolvido para automação fiscal empresarial.

---

**Versão**: 1.0.0  
**Última atualização**: Fevereiro 2026
