import logging
import json
import os
import functools
import time
from datetime import datetime

# --- Formatter Personalizado para JSON ---
class JsonFormatter(logging.Formatter):
    """Formata os logs como objetos JSON (ideal para Splunk, ELK, Datadog)."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger_name": record.name,
            "function": record.funcName,
            "message": record.getMessage(),
            "duration_s": getattr(record, 'duration', 0), # Campo customizado
            "status": getattr(record, 'status', 'INFO')   # Campo customizado
        }
        # Se houver exceção, adiciona ao JSON
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record, ensure_ascii=False)

# --- Classe Base para os Robôs ---
class RPABase:
    def __init__(self, bot_name, base_log_dir="logs"):
        """
        Inicializa o logger específico para este robô.
        :param bot_name: Nome do robô (usado na pasta e arquivos).
        :param base_log_dir: Diretório raiz onde os logs serão salvos.
        """
        self.bot_name = bot_name
        
        # Cria diretório específico para este robô: logs/FinanceiroBot/
        self.bot_log_dir = os.path.join(base_log_dir, bot_name)
        os.makedirs(self.bot_log_dir, exist_ok=True)
        
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(self.bot_name)
        logger.setLevel(logging.INFO)
        logger.handlers = [] # Limpa handlers anteriores para evitar duplicidade
        
        # Data para o nome do arquivo
        today = datetime.now().strftime('%Y-%m-%d')

        # 1. Handler para Arquivo RAW (TXT Simples)
        txt_handler = logging.FileHandler(f"{self.bot_log_dir}/{self.bot_name}_{today}.txt", encoding='utf-8')
        txt_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        txt_handler.setFormatter(txt_formatter)
        logger.addHandler(txt_handler)

        # 2. Handler para Arquivo Estruturado (JSON Lines)
        # Usamos .jsonl pois é mais performático para logs (append linha a linha)
        json_handler = logging.FileHandler(f"{self.bot_log_dir}/{self.bot_name}_{today}.jsonl", encoding='utf-8')
        json_handler.setFormatter(JsonFormatter())
        logger.addHandler(json_handler)

        # 3. Handler para Console (Visualização em tempo real)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(f'[%(levelname)s] {self.bot_name}: %(message)s'))
        logger.addHandler(console_handler)

        return logger

# --- O Decorator ---
def track_step(func):
    """
    Decorator que acessa o 'self.logger' da instância da classe.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Tenta pegar a instância 'self' (primeiro argumento)
        instance = args[0] if args else None
        
        # Verifica se a instância tem o atributo 'logger', senão usa um genérico
        logger = getattr(instance, 'logger', logging.getLogger("GenericBot"))
        
        step_name = func.__name__
        start_time = time.time()

        # Log de Início
        logger.info(f"--> Iniciando etapa: {step_name}", extra={'status': 'START'})

        try:
            result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            # Log de Sucesso (com campo extra de duração para o JSON pegar)
            logger.info(f"<-- Sucesso em: {step_name} ({duration:.2f}s)", 
                        extra={'duration': duration, 'status': 'SUCCESS'})
            return result

        except Exception as e:
            duration = time.time() - start_time
            # Log de Erro
            logger.error(f"!!! Erro em: {step_name} ({duration:.2f}s): {str(e)}", 
                         exc_info=True, 
                         extra={'duration': duration, 'status': 'ERROR'})
            raise e # Repassa o erro para parar o fluxo ou ser tratado acima

    return wrapper