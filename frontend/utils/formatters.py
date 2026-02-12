"""
Formatting utilities for IAudit
"""
import re
from datetime import datetime


def format_cnpj(cnpj) -> str:
    """Format CNPJ as XX.XXX.XXX/XXXX-XX"""
    if cnpj is None: return ""
    digits = list(re.sub(r'\D', '', str(cnpj)))
    if len(digits) != 14:
        return str(cnpj)
    return "{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}".format(*digits)


def mask_cnpj(cnpj) -> str:
    """Mask CNPJ as XX.XXX.XXX/XXXX-XX (hiding middle digits)"""
    if cnpj is None: return ""
    digits = list(re.sub(r'\D', '', str(cnpj)))
    if len(digits) != 14:
        return str(cnpj)
    # Masking middle digits: Index 2 to 7 are replaced with X
    return "{}{}.XXX.XXX/{}{}{}{}-{}{}".format(digits[0], digits[1], digits[8], digits[9], digits[10], digits[11], digits[12], digits[13])


def format_datetime(dt) -> str:
    """Format datetime as DD/MM/YYYY HH:MM"""
    if dt is None or dt == "":
        return "N/A"
    if isinstance(dt, str):
        try:
            # Handle ISO format with or without Z
            dt_str = dt.replace('Z', '+00:00')
            dt = datetime.fromisoformat(dt_str)
        except:
            return str(dt)
    try:
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return str(dt)


def format_date(dt) -> str:
    """Format date as DD/MM/YYYY"""
    if dt is None or dt == "":
        return "N/A"
    if isinstance(dt, str):
        try:
            dt_str = dt.replace('Z', '+00:00')
            dt = datetime.fromisoformat(dt_str)
        except:
            return str(dt)
    try:
        return dt.strftime("%d/%m/%Y")
    except:
        return str(dt)


def get_status_icon(situacao: str) -> str:
    """Get emoji icon for consultation status"""
    status_map = {
        'positiva': '🟢',
        'negativa': '🔴',
        'atualizando': '🟡',
        'erro': '⚪',
        'pendente': '⚪',
        None: '⚪'
    }
    return status_map.get(situacao, '⚪')


def get_status_color(situacao: str) -> str:
    """Get color for status badge"""
    color_map = {
        'positiva': 'green',
        'negativa': 'red',
        'atualizando': 'orange',
        'erro': 'gray',
        'pendente': 'gray',
        None: 'gray'
    }
    return color_map.get(situacao, 'gray')


def format_periodicidade(periodicidade: str) -> str:
    """Format periodicidade for display"""
    map_dict = {
        'diario': 'Diário',
        'semanal': 'Semanal',
        'quinzenal': 'Quinzenal',
        'mensal': 'Mensal'
    }
    return map_dict.get(periodicidade, periodicidade.capitalize())
