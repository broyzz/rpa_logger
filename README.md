# 🤖 RPA Logger Framework

Uma estrutura leve e robusta para padronização de logs em robôs desenvolvidos em Python. 
Utiliza **Decorators** para rastreamento automático de etapas e gera logs simultâneos em formato legível (**TXT**) e estruturado (**JSONL**).

## 🚀 Funcionalidades

- **Log por Robô:** Cada robô possui seu próprio diretório de logs isolado.
- **Decorator `@track_step`:** Calcula automaticamente o tempo de execução e captura exceções.
- **Saída Dupla:**
  - `*.txt`: Para leitura humana rápida.
  - `*.jsonl`: Para ingestão em ferramentas de dados (Power BI, ELK, Splunk, Pandas).
- **Tratamento de Erros:** Exceções são capturadas, logadas com traceback e re-lançadas para o orquestrador.

## 📂 Estrutura do Projeto

```text
.
├── rpa_core.py       # O motor de logs (Classe RPABase e Decorator)
├── meu_robo.py       # Exemplo de implementação do robô
├── .gitignore        # Arquivos ignorados pelo Git
├── README.md         # Documentação
└── meus_logs_rpa/    # (Gerado automaticamente) Contém os logs
    ├── Financeiro/
    └── RH_Bot/