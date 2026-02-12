"""
Mock n8n Server for IAudit Testing
Simulates n8n workflows without needing actual n8n installation
"""

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json

app = Flask(__name__)

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mock n8n Server - IAudit</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }
        .subtitle {
            color: #64748b;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        .status {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            font-weight: 600;
        }
        .workflows {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .workflow-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #667eea;
        }
        .workflow-card h3 {
            color: #1e293b;
            margin-bottom: 0.5rem;
            font-size: 1.3rem;
        }
        .workflow-card p {
            color: #64748b;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            width: 100%;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        }
        .endpoint {
            background: #f1f5f9;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin-top: 0.5rem;
            color: #475569;
        }
        .response {
            background: #1e293b;
            color: #10b981;
            padding: 1rem;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin-top: 1rem;
            display: none;
            white-space: pre-wrap;
        }
        .info {
            background: #dbeafe;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 2rem;
        }
        .info h3 {
            color: #1e40af;
            margin-bottom: 0.5rem;
        }
        .info p {
            color: #1e3a8a;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Mock n8n Server</h1>
        <p class="subtitle">Simulador de Workflows IAudit</p>
        
        <div class="status">
            ✅ Servidor rodando em http://localhost:5678
        </div>
        
        <div class="workflows">
            <div class="workflow-card">
                <h3>📅 Agendador IAudit</h3>
                <p>Busca empresas ativas e agenda consultas automáticas</p>
                <button onclick="testWorkflow('agendador')">Executar Agendador</button>
                <div class="endpoint">GET /webhook/agendador</div>
                <div id="response-agendador" class="response"></div>
            </div>
            
            <div class="workflow-card">
                <h3>🏛️ CND Federal</h3>
                <p>Consulta Certidão Negativa de Débitos Federais</p>
                <button onclick="testWorkflow('cnd-federal')">Testar CND Federal</button>
                <div class="endpoint">POST /webhook/consulta-cnd-federal</div>
                <div id="response-cnd-federal" class="response"></div>
            </div>
            
            <div class="workflow-card">
                <h3>🏢 CND Paraná</h3>
                <p>Consulta Certidão Negativa de Débitos Estaduais (PR)</p>
                <button onclick="testWorkflow('cnd-pr')">Testar CND PR</button>
                <div class="endpoint">POST /webhook/consulta-cnd-pr</div>
                <div id="response-cnd-pr" class="response"></div>
            </div>
            
            <div class="workflow-card">
                <h3>💼 FGTS Regularidade</h3>
                <p>Consulta Certificado de Regularidade do FGTS</p>
                <button onclick="testWorkflow('fgts')">Testar FGTS</button>
                <div class="endpoint">POST /webhook/consulta-fgts</div>
                <div id="response-fgts" class="response"></div>
            </div>
        </div>
        
        <div class="info">
            <h3>💡 Como Usar</h3>
            <p>
                <strong>1.</strong> Clique nos botões acima para testar cada workflow<br>
                <strong>2.</strong> Veja a resposta JSON simulada abaixo de cada botão<br>
                <strong>3.</strong> Use esses endpoints no frontend do IAudit<br>
                <strong>4.</strong> Para produção, substitua por n8n real com credenciais
            </p>
        </div>
    </div>
    
    <script>
        async function testWorkflow(type) {
            const responseDiv = document.getElementById('response-' + type);
            responseDiv.style.display = 'block';
            responseDiv.textContent = 'Executando...';
            
            let url, method, body;
            
            if (type === 'agendador') {
                url = '/webhook/agendador';
                method = 'GET';
            } else if (type === 'cnd-federal') {
                url = '/webhook/consulta-cnd-federal';
                method = 'POST';
                body = JSON.stringify({
                    cnpj: '00000000000191',
                    consulta_id: 'test-' + Date.now()
                });
            } else if (type === 'cnd-pr') {
                url = '/webhook/consulta-cnd-pr';
                method = 'POST';
                body = JSON.stringify({
                    cnpj: '00000000000191',
                    ie_pr: '1234567890',
                    consulta_id: 'test-' + Date.now()
                });
            } else if (type === 'fgts') {
                url = '/webhook/consulta-fgts';
                method = 'POST';
                body = JSON.stringify({
                    cnpj: '00000000000191',
                    consulta_id: 'test-' + Date.now()
                });
            }
            
            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {'Content-Type': 'application/json'},
                    body: body
                });
                const data = await response.json();
                responseDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                responseDiv.textContent = 'Erro: ' + error.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/webhook/agendador', methods=['GET', 'POST'])
def agendador():
    """Simula o workflow Agendador_IAudit"""
    response = {
        "workflow": "Agendador_IAudit",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "message": "Agendador executado com sucesso",
        "empresas_processadas": 5,
        "consultas_agendadas": 15,
        "detalhes": {
            "cnd_federal": 5,
            "cnd_pr": 5,
            "fgts": 5
        }
    }
    return jsonify(response)

@app.route('/webhook/consulta-cnd-federal', methods=['POST'])
def consulta_cnd_federal():
    """Simula o workflow Consulta_CND_Federal"""
    data = request.get_json() or {}
    cnpj = data.get('cnpj', 'N/A')
    consulta_id = data.get('consulta_id', 'N/A')
    
    response = {
        "workflow": "Consulta_CND_Federal",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "input": {
            "cnpj": cnpj,
            "consulta_id": consulta_id
        },
        "resultado": {
            "situacao": "positiva",
            "mensagem": "Certidão Negativa emitida com sucesso",
            "validade": "2026-03-11",
            "pdf_url": f"https://drive.google.com/file/mock/{consulta_id}/cnd_federal.pdf"
        },
        "api_response": {
            "code": 200,
            "provider": "InfoSimples",
            "execution_time": "2.3s"
        }
    }
    return jsonify(response)

@app.route('/webhook/consulta-cnd-pr', methods=['POST'])
def consulta_cnd_pr():
    """Simula o workflow Consulta_CND_PR"""
    data = request.get_json() or {}
    cnpj = data.get('cnpj', 'N/A')
    ie_pr = data.get('ie_pr', 'N/A')
    consulta_id = data.get('consulta_id', 'N/A')
    
    response = {
        "workflow": "Consulta_CND_PR",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "input": {
            "cnpj": cnpj,
            "ie_pr": ie_pr,
            "consulta_id": consulta_id
        },
        "resultado": {
            "situacao": "positiva",
            "mensagem": "Certidão Estadual (PR) emitida com sucesso",
            "validade": "2026-03-11",
            "pdf_url": f"https://drive.google.com/file/mock/{consulta_id}/cnd_pr.pdf"
        },
        "api_response": {
            "code": 200,
            "provider": "InfoSimples",
            "execution_time": "1.8s"
        }
    }
    return jsonify(response)

@app.route('/webhook/consulta-fgts', methods=['POST'])
def consulta_fgts():
    """Simula o workflow Consulta_FGTS"""
    data = request.get_json() or {}
    cnpj = data.get('cnpj', 'N/A')
    consulta_id = data.get('consulta_id', 'N/A')
    
    response = {
        "workflow": "Consulta_FGTS",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "input": {
            "cnpj": cnpj,
            "consulta_id": consulta_id
        },
        "resultado": {
            "situacao": "positiva",
            "mensagem": "Certificado de Regularidade do FGTS emitido",
            "validade": "2026-04-11",
            "pdf_url": f"https://drive.google.com/file/mock/{consulta_id}/fgts.pdf"
        },
        "api_response": {
            "code": 200,
            "provider": "InfoSimples",
            "execution_time": "2.1s"
        }
    }
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Mock n8n Server - IAudit",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Mock n8n Server - IAudit")
    print("=" * 60)
    print("\nServidor iniciado com sucesso!")
    print("\nAcesse: http://localhost:5678")
    print("\nEndpoints disponiveis:")
    print("   - Dashboard: http://localhost:5678/")
    print("   - Agendador: http://localhost:5678/webhook/agendador")
    print("   - CND Federal: http://localhost:5678/webhook/consulta-cnd-federal")
    print("   - CND PR: http://localhost:5678/webhook/consulta-cnd-pr")
    print("   - FGTS: http://localhost:5678/webhook/consulta-fgts")
    print("\nPressione Ctrl+C para parar o servidor")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5678, debug=True)
