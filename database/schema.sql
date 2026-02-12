-- 4. ARQUITETURA DE DADOS (SUPABASE)

-- 4.1 Tabela: empresas
create table if not exists empresas (
 id uuid default gen_random_uuid() primary key,
 cnpj text not null unique,
 razao_social text not null,
 inscricao_estadual_pr text,
 email_notificacao text,
 whatsapp text,
 
 -- Configuração de agendamento
 periodicidade text not null check (periodicidade in ('diario', 'semanal', 'quinzenal', 'mensal')),
 dia_semana integer, -- 0=domingo, 1=segunda... (se semanal)
 dia_mes integer, -- 1-31 (se mensal)
 horario time not null default '08:00:00',
 
 -- Controle
 ativo boolean default true,
 created_at timestamp with time zone default now(),
 updated_at timestamp with time zone default now()
);

-- Índices empresas
create index if not exists idx_empresas_cnpj on empresas(cnpj);
create index if not exists idx_empresas_ativo on empresas(ativo);


-- 4.2 Tabela: consultas
create table if not exists consultas (
 id uuid default gen_random_uuid() primary key,
 empresa_id uuid references empresas(id) on delete cascade,
 
 -- Tipo e status
 tipo text not null check (tipo in ('cnd_federal', 'cnd_pr', 'fgts_regularidade')),
 status text not null check (status in ('agendada', 'processando', 'concluida', 'erro')),
 
 -- Resultado
 situacao text check (situacao in ('positiva', 'negativa', 'atualizando', 'erro', null)),
 resultado_json jsonb,
 pdf_url text,
 mensagem_erro text,
 
 -- Datas
 data_agendada timestamp with time zone,
 data_execucao timestamp with time zone,
 data_validade date,
 
 -- Metadados
 tentativas integer default 0,
 created_at timestamp with time zone default now()
);

-- Índices consultas
create index if not exists idx_consultas_empresa on consultas(empresa_id);
create index if not exists idx_consultas_tipo_status on consultas(tipo, status);
create index if not exists idx_consultas_data_agendada on consultas(data_agendada);


-- 4.3 Tabela: logs_execucao
create table if not exists logs_execucao (
 id uuid default gen_random_uuid() primary key,
 consulta_id uuid references consultas(id) on delete cascade,
 nivel text check (nivel in ('info', 'aviso', 'erro')),
 mensagem text not null,
 payload jsonb,
 created_at timestamp with time zone default now()
);


-- 4.4 Tabela: usuarios
create table if not exists usuarios (
 id uuid default gen_random_uuid() primary key,
 email text not null unique,
 nome text not null,
 perfil text default 'operador' check (perfil in ('admin', 'operador')),
 ativo boolean default true,
 created_at timestamp with time zone default now()
);


-- 4.5 Row Level Security (RLS)
-- Ativar RLS em todas as tabelas
alter table empresas enable row level security;
alter table consultas enable row level security;

-- Política básica (ajustar conforme necessidade de multi-tenancy)
create policy "Allow all" on empresas for all using (true) with check (true);
create policy "Allow all" on consultas for all using (true) with check (true);
