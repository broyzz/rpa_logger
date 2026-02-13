from rpa_logger import RPABase, track_step
import time

# --- Robô 1: Robô Financeiro ---
class RoboFinanceiro(RPABase):
    
    def __init__(self):
        # Configura o logger criando a pasta "logs/Financeiro_v1"
        super().__init__(bot_name="Financeiro_v1", base_log_dir="meus_logs_rpa")

    @track_step
    def login_sap(self, usuario):
        time.sleep(0.5)
        self.logger.info(f"Digitando credenciais para {usuario}...")
    
    @track_step
    def extrair_relatorio(self):
        time.sleep(1.0)
        # Simulando uma lógica de negócio
        registros = 500
        self.logger.info(f"Relatório extraído com {registros} linhas.")
        return registros

# --- Robô 2: Robô de RH (Com erro proposital) ---
class RoboRH(RPABase):
    
    def __init__(self):
        # Cria pasta separada "logs/RH_Bot"
        super().__init__(bot_name="RH_Bot", base_log_dir="meus_logs_rpa")

    @track_step
    def processar_ferias(self):
        time.sleep(0.5)
        self.logger.info("Lendo planilha de férias...")
        # Erro proposital
        raise ValueError("Planilha não encontrada na rede!")

# --- Execução ---
if __name__ == "__main__":
    
    # Executa o Financeiro
    print("--- Rodando Financeiro ---")
    bot_fin = RoboFinanceiro()
    bot_fin.login_sap("admin_financeiro")
    bot_fin.extrair_relatorio()

    # Executa o RH
    print("\n--- Rodando RH ---")
    bot_rh = RoboRH()
    try:
        bot_rh.processar_ferias()
    except Exception:
        print("Robô de RH falhou (como esperado).")