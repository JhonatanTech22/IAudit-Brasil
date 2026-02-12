"""
Validation utilities for IAudit
"""
import re


def validate_cnpj_format(cnpj: str) -> bool:
    """Check if CNPJ has valid format"""
    # Remove non-digits
    cnpj = re.sub(r'\D', '', cnpj)
    return len(cnpj) == 14


def validate_cnpj_checksum(cnpj: str) -> bool:
    """Validate CNPJ checksum digits"""
    # Remove non-digits
    cnpj = re.sub(r'\D', '', cnpj)
    
    if len(cnpj) != 14:
        return False
    
    # Check if all digits are the same
    if cnpj == cnpj[0] * 14:
        return False
    
    # Calculate first check digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(12))
    remainder = sum_digits % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    
    if int(cnpj[12]) != digit1:
        return False
    
    # Calculate second check digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(13))
    remainder = sum_digits % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    
    return int(cnpj[13]) == digit2


def validate_cnpj(cnpj: str) -> tuple[bool, str]:
    """
    Validate CNPJ completely
    Returns: (is_valid, error_message)
    """
    if not cnpj or not cnpj.strip():
        return False, "CNPJ não pode estar vazio"
    
    if not validate_cnpj_format(cnpj):
        return False, "CNPJ deve ter 14 dígitos"
    
    if not validate_cnpj_checksum(cnpj):
        return False, "CNPJ inválido (dígitos verificadores incorretos)"
    
    return True, ""


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return True  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate Brazilian phone number"""
    if not phone:
        return True  # Phone is optional
    # Remove non-digits
    digits = re.sub(r'\D', '', phone)
    # Brazilian phones: 10 or 11 digits (with area code)
    return len(digits) in [10, 11]
