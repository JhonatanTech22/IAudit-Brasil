"""
Mock data for IAudit demonstration
"""
from datetime import datetime, timedelta
import random


def get_mock_empresas():
    """Get mock companies data"""
    empresas = [
        {
            'id': '1',
            'cnpj': '12345678000195',
            'razao_social': 'Tech Solutions Ltda',
            'inscricao_estadual_pr': '1234567890',
            'email_notificacao': 'contato@techsolutions.com.br',
            'whatsapp': '41999887766',
            'periodicidade': 'semanal',
            'horario': '08:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=30)
        },
        {
            'id': '2',
            'cnpj': '98765432000187',
            'razao_social': 'Comércio Brasil S.A.',
            'inscricao_estadual_pr': '9876543210',
            'email_notificacao': 'fiscal@comerciobrasil.com.br',
            'whatsapp': '41988776655',
            'periodicidade': 'mensal',
            'horario': '09:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=60)
        },
        {
            'id': '3',
            'cnpj': '11223344000156',
            'razao_social': 'Indústria Paraná Ltda',
            'inscricao_estadual_pr': '1122334455',
            'email_notificacao': 'admin@industriapr.com.br',
            'whatsapp': '41977665544',
            'periodicidade': 'quinzenal',
            'horario': '10:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=45)
        },
        {
            'id': '4',
            'cnpj': '55667788000123',
            'razao_social': 'Serviços Curitiba ME',
            'inscricao_estadual_pr': '5566778899',
            'email_notificacao': 'contato@servicosctba.com.br',
            'whatsapp': '41966554433',
            'periodicidade': 'semanal',
            'horario': '08:30:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=15)
        },
        {
            'id': '5',
            'cnpj': '99887766000145',
            'razao_social': 'Distribuidora Sul Ltda',
            'inscricao_estadual_pr': '9988776655',
            'email_notificacao': 'fiscal@distribuidorasul.com.br',
            'whatsapp': '41955443322',
            'periodicidade': 'mensal',
            'horario': '14:00:00',
            'ativo': False,
            'created_at': datetime.now() - timedelta(days=90)
        },
        {
            'id': '6',
            'cnpj': '44332211000109',
            'razao_social': 'Fazenda Sol Nascente',
            'inscricao_estadual_pr': '4433221100',
            'email_notificacao': 'agro@solnascente.com.br',
            'whatsapp': '41944332211',
            'periodicidade': 'diario',
            'horario': '07:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=120)
        },
        {
            'id': '7',
            'cnpj': '88776655000199',
            'razao_social': 'Supermercado Avenida',
            'inscricao_estadual_pr': '8877665544',
            'email_notificacao': 'financeiro@superavenida.com.br',
            'whatsapp': '41933221100',
            'periodicidade': 'semanal',
            'horario': '20:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=200)
        },
        {
            'id': '8',
            'cnpj': '22446688000177',
            'razao_social': 'Clínica Santa Helena',
            'inscricao_estadual_pr': '2244668800',
            'email_notificacao': 'adm@santahelena.com.br',
            'whatsapp': '41922110099',
            'periodicidade': 'mensal',
            'horario': '11:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=10)
        },
        {
            'id': '9',
            'cnpj': '33557799000188',
            'razao_social': 'Transportadora Rápida PR',
            'inscricao_estadual_pr': '3355779900',
            'email_notificacao': 'log@rapidapr.com.br',
            'whatsapp': '41911009988',
            'periodicidade': 'diario',
            'horario': '05:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=150)
        },
        {
            'id': '10',
            'cnpj': '12121212000112',
            'razao_social': 'Hotel Bella Vista',
            'inscricao_estadual_pr': '1212121212',
            'email_notificacao': 'reservas@bellavista.com.br',
            'whatsapp': '41900998877',
            'periodicidade': 'quinzenal',
            'horario': '16:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=300)
        },
        {
            'id': '11',
            'cnpj': '21212121000121',
            'razao_social': 'Metalúrgica Norte',
            'inscricao_estadual_pr': '2121212121',
            'email_notificacao': 'prod@metnorte.com.br',
            'whatsapp': '41999775533',
            'periodicidade': 'semanal',
            'horario': '07:30:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=25)
        },
        {
            'id': '12',
            'cnpj': '32323232000132',
            'razao_social': 'Restaurante Sabores',
            'inscricao_estadual_pr': '3232323232',
            'email_notificacao': 'chef@sabores.com.br',
            'whatsapp': '41988664422',
            'periodicidade': 'mensal',
            'horario': '23:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=50)
        },
        {
            'id': '13',
            'cnpj': '43434343000143',
            'razao_social': 'Academia BioFit',
            'inscricao_estadual_pr': '4343434343',
            'email_notificacao': 'treino@biofit.com.br',
            'whatsapp': '41977553311',
            'periodicidade': 'semanal',
            'horario': '06:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=80)
        },
        {
            'id': '14',
            'cnpj': '54545454000154',
            'razao_social': 'Construtora Aliança',
            'inscricao_estadual_pr': '5454545454',
            'email_notificacao': 'obra@alianca.com.br',
            'whatsapp': '41966442200',
            'periodicidade': 'quinzenal',
            'horario': '09:30:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=365)
        },
        {
            'id': '15',
            'cnpj': '65656565000165',
            'razao_social': 'Consultoria Prisma',
            'inscricao_estadual_pr': '6565656565',
            'email_notificacao': 'socio@prisma.com.br',
            'whatsapp': '41955331199',
            'periodicidade': 'mensal',
            'horario': '10:30:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=12)
        },
        {
            'id': '16',
            'cnpj': '76767676000176',
            'razao_social': 'Auto Posto Central',
            'inscricao_estadual_pr': '7676767676',
            'email_notificacao': 'gerente@postocentral.com.br',
            'whatsapp': '41944220088',
            'periodicidade': 'diario',
            'horario': '00:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=500)
        },
        {
            'id': '17',
            'cnpj': '87878787000187',
            'razao_social': 'Padaria Pão de Mel',
            'inscricao_estadual_pr': '8787878787',
            'email_notificacao': 'faleconosco@paodemel.com.br',
            'whatsapp': '41933119977',
            'periodicidade': 'semanal',
            'horario': '04:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=180)
        },
        {
            'id': '18',
            'cnpj': '98989898000198',
            'razao_social': 'Gráfica Expressa',
            'inscricao_estadual_pr': '9898989898',
            'email_notificacao': 'arte@expressa.com.br',
            'whatsapp': '41922008866',
            'periodicidade': 'mensal',
            'horario': '13:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=40)
        },
        {
            'id': '19',
            'cnpj': '09090909000109',
            'razao_social': 'Drogaria Saúde',
            'inscricao_estadual_pr': '0909090909',
            'email_notificacao': 'farmaceutico@saude.com.br',
            'whatsapp': '41911997755',
            'periodicidade': 'diario',
            'horario': '08:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=250)
        },
        {
            'id': '20',
            'cnpj': '10101010000110',
            'razao_social': 'Móveis Estrela',
            'inscricao_estadual_pr': '1010101010',
            'email_notificacao': 'vendas@movestelar.com.br',
            'whatsapp': '41900886644',
            'periodicidade': 'semanal',
            'horario': '15:00:00',
            'ativo': True,
            'created_at': datetime.now() - timedelta(days=320)
        }
    ]
    return empresas


def get_mock_consultas():
    """Get mock consultation data"""
    empresas = get_mock_empresas()
    consultas = []
    
    tipos = ['cnd_federal', 'cnd_pr', 'fgts']
    situacoes = ['positiva', 'positiva', 'positiva', 'negativa', 'positiva']
    
    for empresa in empresas:
        for tipo in tipos:
            # Create recent consultation
            situacao = random.choice(situacoes)
            
            # Specific cases for variety
            if empresa['id'] in ['3', '7', '14'] and tipo == 'fgts':
                situacao = 'negativa'
            if empresa['id'] in ['9', '19'] and tipo == 'cnd_pr':
                situacao = 'negativa'
            if empresa['id'] == '5':
                situacao = 'erro'
                
            consulta = {
                'id': f"{empresa['id']}-{tipo}-1",
                'empresa_id': empresa['id'],
                'tipo': tipo,
                'status': 'concluida',
                'situacao': situacao,
                'resultado_json': {},
                'pdf_url': f"https://drive.google.com/file/{empresa['id']}/{tipo}/latest.pdf",
                'data_execucao': datetime.now() - timedelta(hours=random.randint(1, 48)),
                'data_validade': datetime.now() + timedelta(days=random.randint(10, 60)),
                'tentativas': 1,
                'created_at': datetime.now() - timedelta(hours=random.randint(1, 48))
            }
            consultas.append(consulta)
            
            # Add historical data
            for i in range(3):
                hist_consulta = {
                    'id': f"{empresa['id']}-{tipo}-{i+2}",
                    'empresa_id': empresa['id'],
                    'tipo': tipo,
                    'status': 'concluida',
                    'situacao': 'positiva' if random.random() > 0.1 else 'negativa',
                    'resultado_json': {},
                    'pdf_url': f"https://drive.google.com/file/{empresa['id']}/{tipo}/hist_{i}.pdf",
                    'data_execucao': datetime.now() - timedelta(days=7*(i+1)),
                    'data_validade': datetime.now() - timedelta(days=7*i) + timedelta(days=30),
                    'tentativas': 1,
                    'created_at': datetime.now() - timedelta(days=7*(i+1))
                }
                consultas.append(hist_consulta)
    
    return consultas


def get_latest_consultas_by_empresa():
    """Get latest consultation for each company and type"""
    consultas = get_mock_consultas()
    empresas = get_mock_empresas()
    
    result = {}
    for empresa in empresas:
        result[empresa['id']] = {
            'empresa': empresa,
            'consultas': {
                'cnd_federal': None,
                'cnd_pr': None,
                'fgts': None
            }
        }
    
    # Get latest for each type
    for consulta in consultas:
        empresa_id = consulta['empresa_id']
        tipo = consulta['tipo']
        
        if result[empresa_id]['consultas'][tipo] is None or \
           consulta['data_execucao'] > result[empresa_id]['consultas'][tipo]['data_execucao']:
            result[empresa_id]['consultas'][tipo] = consulta
    
    return result


def get_dashboard_stats():
    """Get dashboard statistics"""
    empresas = get_mock_empresas()
    consultas = get_mock_consultas()
    
    active_companies = sum(1 for e in empresas if e['ativo'])
    
    today = datetime.now().date()
    today_consultas = [c for c in consultas if c['data_execucao'].date() == today]
    
    completed = [c for c in consultas if c['status'] == 'concluida']
    success_rate = (sum(1 for c in completed if c['situacao'] == 'positiva') / len(completed) * 100) if completed else 0
    
    alerts = [c for c in consultas if c['situacao'] in ['negativa', 'erro'] and 
              c['data_execucao'] > datetime.now() - timedelta(days=7)]
    
    # Last 7 days data
    chart_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=6-i)
        count = sum(1 for c in consultas if c['data_execucao'].date() == date.date())
        chart_data.append({
            'data': date,
            'consultas': count if count > 0 else random.randint(80, 130)
        })
    
    # Sort alerts by date to show most recent
    alerts.sort(key=lambda x: x['data_execucao'], reverse=True)
    
    # Add company name to alerts for the table
    for alert in alerts:
        emp = next((e for e in empresas if e['id'] == alert['empresa_id']), None)
        alert['empresa_nome'] = emp['razao_social'] if emp else "N/A"
    
    return {
        'empresas_ativas': active_companies,
        'consultas_hoje': len(today_consultas),
        'taxa_sucesso': round(success_rate, 1),
        'alertas_pendentes': len(alerts),
        'chart_data': chart_data,
        'alertas_recentes': alerts[:5]
    }
