import os
import streamlit as st
import pandas as pd
from utils.mock_data import get_mock_empresas, get_latest_consultas_by_empresa
from dotenv import load_dotenv

load_dotenv()

# This class handles the abstraction between Supabase (Production) and Mock (Development)
class DataLayer:
    def __init__(self):
        self.use_mock = not os.getenv("SUPABASE_URL")
        try:
            # Initialize session state for mock persistence if we don't have a DB
            if self.use_mock and "mock_db" not in st.session_state:
                st.session_state.mock_db = get_mock_empresas()
                st.session_state.mock_consultas = get_latest_consultas_by_empresa()
        except:
            # Not in a streamlit context, maybe background or loading
            pass

    def get_empresas(self):
        if self.use_mock:
            return st.session_state.mock_db
        # TODO: Add real Supabase query here
        return get_mock_empresas()

    def get_empresa_by_id(self, empresa_id):
        empresas = self.get_empresas()
        return next((e for e in empresas if e['id'] == empresa_id), None)

    def insert_empresas(self, new_empresas_df):
        """Adds new companies to the system"""
        if self.use_mock:
            current = st.session_state.mock_db
            max_id = max([int(e['id']) for e in current]) if current else 0
            
            for _, row in new_empresas_df.iterrows():
                max_id += 1
                new_entry = {
                    'id': str(max_id),
                    'cnpj': row['CNPJ'],
                    'razao_social': row['Razao Social'],
                    'inscricao_estadual_pr': row.get('IE_PR', ''),
                    'email_notificacao': row.get('Email', ''),
                    'whatsapp': row.get('WhatsApp', ''),
                    'periodicidade': 'semanal',
                    'ativo': True
                }
                current.append(new_entry)
            st.session_state.mock_db = current
            return True
        return False # real DB integration pending

    def get_latest_status(self):
        """Gets summarized status for all companies"""
        if self.use_mock:
            return st.session_state.mock_consultas
        return get_latest_consultas_by_empresa()

# Singleton instance
db = DataLayer()
