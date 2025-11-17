# 🎯 Debatedores - Framework de Debates Multi-Agente

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Debatedores** é um framework extensível para conduzir debates estruturados entre múltiplos agentes de IA, com suporte a documentos via RAG (Retrieval-Augmented Generation) e métricas de convergência.

## ✨ Características Principais

- 🤖 **Multi-Provider**: Suporte para OpenAI, Google Gemini e extensível para outros
- 📄 **RAG Integrado**: Processa PDFs, Markdown e páginas web
- 🎭 **Agentes Customizáveis**: Crie agentes com diferentes personas e objetivos
- 📊 **Métricas Plugáveis**: Sistema extensível de métricas de convergência
- 🔄 **Estratégias Flexíveis**: Múltiplas estratégias de debate (adversarial, consenso, etc.)
- 🎨 **Múltiplos Formatos**: Saída em JSON, Markdown, HTML
- ⚙️ **Configuração via YAML**: Parametrize debates facilmente
- 🧪 **Testado**: Cobertura de testes unitários

---

## 📦 Instalação

### Via pip (recomendado)

```bash
pip install debatedores
```

### Via clone do repositório

```bash
git clone https://github.com/cbaracho200/debatedores_llm.git
cd debatedores_llm
pip install -e .
```

### Instalação de Desenvolvimento

```bash
pip install -e ".[dev]"
```

---

## 🚀 Início Rápido

### 1. Configure suas API Keys

```bash
export OPENAI_API_KEY="sua-chave-openai"
# ou
export GEMINI_API_KEY="sua-chave-gemini"
```

### 2. Primeiro Debate

```python
import asyncio
from debatedores.providers import OpenAIProvider
from debatedores.agents import Agent, ADVOCATUS_CONFIG, DIABOLI_CONFIG
from debatedores.strategies import AdversarialDebate

async def main():
    # Configurar provider e agentes
    provider = OpenAIProvider()
    llm = provider.get_llm()

    agents = [
        Agent(ADVOCATUS_CONFIG, llm),
        Agent(DIABOLI_CONFIG, llm)
    ]

    # Executar debate
    strategy = AdversarialDebate()
    result = await strategy.execute_round(
        round_number=1,
        agents=agents,
        context="PERGUNTA: IA deve ser regulamentada?"
    )

    # Exibir resultados
    print(f"Agreement Score: {result.agreement_score:.0%}")
    print(f"Síntese: {result.synthesis}")

asyncio.run(main())
```

---

## 📚 Documentação

### Arquitetura do Framework

```
debatedores/
├── core/           # Modelos e eventos principais
├── providers/      # Abstrações de LLM (OpenAI, Gemini, etc.)
├── processors/     # Processadores de documentos (PDF, MD, Web)
├── metrics/        # Sistema de métricas de convergência
├── agents/         # Sistema de agentes configuráveis
├── strategies/     # Estratégias de debate
├── stopping/       # Critérios de parada
├── formatters/     # Formatadores de saída
├── prompts/        # Templates de prompts
└── config/         # Sistema de configuração
```

### Componentes Principais

#### 1. Providers

Abstrações para diferentes provedores de LLM:

```python
from debatedores.providers import OpenAIProvider, GeminiProvider

# OpenAI
provider = OpenAIProvider(api_key="...")
llm = provider.get_llm(model_name="gpt-4", temperature=0.7)

# Gemini
provider = GeminiProvider(api_key="...")
llm = provider.get_llm(model_name="gemini-2.5-pro")
```

#### 2. Agents

Agentes com configurações customizadas:

```python
from debatedores.agents import Agent, AgentConfig

config = AgentConfig(
    name="Analista Técnico",
    role="technical_analyst",
    system_prompt="Você é um analista técnico especializado...",
    temperature=0.6
)

agent = Agent(config, llm)
```

#### 3. Processadores de Documentos

```python
from debatedores.processors import PDFProcessor, MarkdownProcessor

# Processar PDF
processor = PDFProcessor()
documents = await processor.process("paper.pdf")

# Processar Markdown
md_processor = MarkdownProcessor()
docs = await md_processor.process("article.md")
```

#### 4. Métricas

```python
from debatedores.metrics import AgreementScore, SemanticSimilarity, MetricsAggregator

# Métrica simples
metric = AgreementScore()
score = metric.calculate(perspective1, perspective2)

# Múltiplas métricas
aggregator = MetricsAggregator(
    metrics=[AgreementScore(), SemanticSimilarity()],
    weights=[0.6, 0.4]
)
results = aggregator.aggregate(perspective1, perspective2)
```

#### 5. Critérios de Parada

```python
from debatedores.stopping import AgreementThreshold, MaxRounds, StoppingManager

manager = StoppingManager(criteria=[
    AgreementThreshold(0.8),
    MaxRounds(10)
])

should_stop, reason = manager.evaluate(debate_state)
```

#### 6. Formatadores

```python
from debatedores.formatters import JSONFormatter, MarkdownFormatter, HTMLFormatter

# JSON
json_fmt = JSONFormatter()
output = json_fmt.format(final_result)

# Markdown
md_fmt = MarkdownFormatter()
output = md_fmt.format(final_result)

# HTML
html_fmt = HTMLFormatter()
output = html_fmt.format(final_result)
```

---

## 📖 Exemplos

### Debate com PDFs

```python
from debatedores.processors import PDFProcessor
from llama_index.core import VectorStoreIndex

# Processar PDF
processor = PDFProcessor()
documents = await processor.process("research.pdf")

# Criar índice
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Executar debate com contexto dos documentos
result = await strategy.execute_round(
    round_number=1,
    agents=agents,
    context="Analise o paper e discuta a metodologia",
    query_engine=query_engine
)
```

### Agentes Customizados

```python
from debatedores.agents import AgentConfig, Agent

# Criar configurações personalizadas
optimist = AgentConfig(
    name="Otimista",
    role="optimist",
    system_prompt="Foque em oportunidades e benefícios...",
    temperature=0.8
)

pessimist = AgentConfig(
    name="Pessimista",
    role="pessimist",
    system_prompt="Identifique riscos e desafios...",
    temperature=0.6
)

agents = [Agent(optimist, llm), Agent(pessimist, llm)]
```

### Usando Configuração YAML

```yaml
# config.yaml
debate:
  max_rounds: 5
  agreement_target: 0.8
  temperature: 0.7

llm:
  provider: "openai"
  model_name: "gpt-4"
```

```python
from debatedores.config import FrameworkConfig

config = FrameworkConfig.from_yaml("config.yaml")
```

Mais exemplos em [`examples/`](./examples/)

---

## 🧪 Testes

Executar testes unitários:

```bash
pytest tests/
```

Com cobertura:

```bash
pytest --cov=debatedores --cov-report=html
```

---

## 🏗️ Extensibilidade

### Criar um Provider Customizado

```python
from debatedores.providers.base import LLMProvider

class MyCustomProvider(LLMProvider):
    def get_llm(self, model_name=None, temperature=0.7, **kwargs):
        # Implementação
        pass

    def get_embeddings(self, model_name=None, **kwargs):
        # Implementação
        pass

    def get_provider_name(self):
        return "my_custom_provider"
```

### Criar uma Métrica Customizada

```python
from debatedores.metrics.base import DebateMetric

class CustomMetric(DebateMetric):
    def calculate(self, agent1, agent2):
        # Sua lógica de métrica
        return score  # 0.0 a 1.0
```

### Criar uma Estratégia Customizada

```python
from debatedores.strategies.base import DebateStrategy

class ConsensusStrategy(DebateStrategy):
    async def execute_round(self, round_number, agents, context, query_engine=None):
        # Sua lógica de estratégia
        return debate_round
```

---

## 🗺️ Roadmap

- [x] Core framework
- [x] Multi-provider support (OpenAI, Gemini)
- [x] Document processors (PDF, Markdown, Web)
- [x] Metrics system
- [x] Stopping criteria
- [x] Output formatters
- [ ] Anthropic provider
- [ ] Workflow completo multi-rodada
- [ ] UI para visualização de debates
- [ ] Suporte a mais formatos de documentos
- [ ] Sistema de cache avançado
- [ ] Métricas de qualidade argumentativa
- [ ] Estratégias de consenso e chain-of-thought

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha cobertura de testes acima de 80%
- Siga PEP 8 e use type hints
- Documente novas funcionalidades
- Adicione exemplos quando apropriado

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- [LlamaIndex](https://www.llamaindex.ai/) - Framework RAG
- [Pydantic](https://pydantic.dev/) - Validação de dados
- Comunidade open source

---

## 📞 Contato

- **Repositório**: [github.com/cbaracho200/debatedores_llm](https://github.com/cbaracho200/debatedores_llm)
- **Issues**: [github.com/cbaracho200/debatedores_llm/issues](https://github.com/cbaracho200/debatedores_llm/issues)

---

## 📊 Status do Projeto

**Versão Atual**: 0.1.0 (Alpha)

**Status**: 🚧 Em desenvolvimento ativo

O framework está funcional mas ainda em desenvolvimento. APIs podem mudar até a versão 1.0.0.
