# utils/validator.py
import re

def validar_email(email):
    """Validación de email usando Expresión Regular ."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def validar_campo_numerico(texto):
    """Validación estricta que rechaza caracteres no numéricos ."""
    return texto.isdigit()

def validar_longitud_texto(texto, min_len=0, max_len=float('inf')):
    """Validación de longitud mínima/máxima ."""
    longitud = len(texto)
    return min_len <= longitud <= max_len