"""Module for CNPJ validator"""


def is_valid_cnpj(cnpj: str):
    """Custom CNPJ validator
    Args:
        cnpj (str): CNPJ in format string

    Returns:
        bool: Boolean indication wether the CNPJ is valid
    """
    cnpj_digits = cnpj.replace('.', '').replace('/', '').replace('-', '')
    return len(cnpj_digits) == 14
