import requests
import json
import os

N8N_URL = "https://n8n2.allanturing.com/api/v1/workflows"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYzNlY2IyMC1iMWQ5LTQzZjYtYWVjZi1mMGI5MTgyNjkzMmUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwNzQzOTI0fQ.QG28qLmL_nNZcSo_0t-8GYTVQQrzQ7ZY8o_OhQG3WpY"

WORKFLOW_FILES = [
    "Agendador_IAudit.json",
    "Consulta_CND_Federal.json",
    "Consulta_CND_PR.json",
    "Consulta_FGTS.json"
]

HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def upload_workflows():
    success_count = 0
    for filename in WORKFLOW_FILES:
        path = os.path.join("n8n", "workflows", filename)
        print(f"Uploading {filename}...")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Extract only allowed properties for creation
            # POST /workflows typically needs: name, nodes, connections, settings
            workflow_data = {
                "name": raw_data.get("name"),
                "nodes": raw_data.get("nodes"),
                "connections": raw_data.get("connections"),
                "settings": raw_data.get("settings", {})
            }
            
            # Remove IDs inside nodes just in case, though usually fine
            # for node in workflow_data["nodes"]:
            #    if "id" in node: del node["id"]
            
            response = requests.post(N8N_URL, headers=HEADERS, json=workflow_data)
            
            if response.status_code in [200, 201]:
                workflow_id = response.json().get('id')
                print(f"Successfully uploaded {filename}. ID: {workflow_id}")
                
                # Try to activate
                activate_url = f"{N8N_URL}/{workflow_id}"
                print(f"Activating {workflow_id}...")
                
                # n8n V1 update requires full object
                activation_data = workflow_data.copy()
                activation_data["active"] = True
                
                activate_response = requests.put(activate_url, headers=HEADERS, json=activation_data)
                
                if activate_response.status_code == 200:
                    print(f"Successfully activated {filename}.")
                else:
                    print(f"Failed to activate {filename}. Status: {activate_response.status_code}")
                    print(f"Response: {activate_response.text}")
                
                success_count += 1
            else:
                print(f"Failed to upload {filename}. Status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            
    print(f"\nUpload complete. {success_count}/{len(WORKFLOW_FILES)} workflows uploaded successfully.")

if __name__ == "__main__":
    upload_workflows()
