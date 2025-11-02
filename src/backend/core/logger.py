"""
LOGGER CONFIGURADO - EnergyFlow AI
Sistema de logging centralizado para toda a aplicação.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Criar diretório de logs se não existir
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configurar formato de log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Configura e retorna um logger com handlers para console e arquivo.
    
    Args:
        name: Nome do logger (geralmente __name__)
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Handler para arquivo
    log_file = LOG_DIR / f"energyflow_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Adicionar handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Logger padrão da aplicação
app_logger = setup_logger("energyflow", "INFO")
