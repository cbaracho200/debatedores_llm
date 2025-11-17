# Exemplos de Uso - Debatedores Framework

Esta pasta contém exemplos práticos de uso do framework Debatedores.

## 📋 Lista de Exemplos

### 1. `basic_debate.py`
Exemplo mais simples - debate básico entre dois agentes sem documentos.

**Uso:**
```bash
python examples/basic_debate.py
```

**Aprende:**
- Como configurar um provider
- Como criar agentes
- Como executar uma rodada de debate
- Como interpretar os resultados

---

### 2. `debate_with_pdfs.py`
Debate fundamentado em documentos PDF.

**Pré-requisitos:**
- PDFs na pasta `documentos/`

**Uso:**
```bash
python examples/debate_with_pdfs.py
```

**Aprende:**
- Como processar PDFs
- Como criar índices vetoriais
- Como integrar documentos no debate
- Como agentes consultam evidências

---

### 3. `custom_agents.py`
Criação de agentes com configurações personalizadas.

**Uso:**
```bash
python examples/custom_agents.py
```

**Aprende:**
- Como criar AgentConfig customizado
- Como ajustar temperatura e comportamento
- Como usar diferentes providers (Gemini)
- Como criar personas específicas

---

### 4. `with_config_file.py`
Uso de arquivo de configuração YAML.

**Uso:**
```bash
python examples/with_config_file.py
```

**Aprende:**
- Como carregar configurações de arquivo
- Como parametrizar debates
- Como salvar/compartilhar configurações
- Como usar diferentes providers via config

---

## 🚀 Começando

### Instalação
```bash
# Instalar o framework
pip install -e .

# Ou instalar dependências manualmente
pip install -r requirements.txt
```

### Configuração de API Keys

**OpenAI:**
```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

**Google Gemini:**
```bash
export GEMINI_API_KEY="sua-chave-aqui"
```

### Execução
```bash
# Executar qualquer exemplo
python examples/<nome_do_exemplo>.py
```

---

## 📚 Exemplos Avançados (em breve)

- `multiple_strategies.py` - Comparando diferentes estratégias
- `custom_metrics.py` - Criando métricas personalizadas
- `formatters_showcase.py` - Usando diferentes formatadores
- `web_documents.py` - Debatendo sobre páginas web
- `full_debate_workflow.py` - Debate completo multi-rodada

---

## 🆘 Ajuda

Se tiver problemas executando os exemplos:

1. Verifique se as dependências estão instaladas
2. Confirme que as API keys estão configuradas
3. Para exemplos com PDFs, certifique-se que os arquivos existem
4. Consulte a documentação principal no `README.md`

---

## 💡 Contribuindo

Tem um exemplo interessante? Contribua! Envie um PR com:
- Código do exemplo
- Descrição clara do que demonstra
- Instruções de uso
- Atualização deste README
