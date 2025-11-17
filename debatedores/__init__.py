"""
Debatedores - Framework para debates multi-agente com RAG

Um framework extensível para conduzir debates estruturados entre
múltiplos agentes de IA, com suporte a documentos e métricas de convergência.

Exemplo básico:
    >>> from debatedores import DebateFramework
    >>> from debatedores.providers import OpenAIProvider
    >>>
    >>> framework = DebateFramework(provider=OpenAIProvider())
    >>> result = await framework.debate(
    ...     question="Qual a melhor abordagem?",
    ...     documents=["paper.pdf"]
    ... )
"""

__version__ = "0.1.0"
__author__ = "Debatedores Team"
__license__ = "MIT"

# Core models
from debatedores.core.models import (
    AgentPerspective,
    DebateRound,
    DebateState,
    FinalResult,
)

# Providers
from debatedores.providers import (
    LLMProvider,
    OpenAIProvider,
    GeminiProvider,
)

# Processors
from debatedores.processors import (
    DocumentProcessor,
    PDFProcessor,
    MarkdownProcessor,
    WebProcessor,
)

# Metrics
from debatedores.metrics import (
    DebateMetric,
    AgreementScore,
    SemanticSimilarity,
    MetricsAggregator,
)

# Agents
from debatedores.agents import (
    AgentConfig,
    Agent,
    ADVOCATUS_CONFIG,
    DIABOLI_CONFIG,
)

# Stopping criteria
from debatedores.stopping import (
    StoppingCriterion,
    AgreementThreshold,
    MaxRounds,
    StoppingManager,
)

# Strategies
from debatedores.strategies import (
    DebateStrategy,
    AdversarialDebate,
)

# Formatters
from debatedores.formatters import (
    OutputFormatter,
    JSONFormatter,
    MarkdownFormatter,
    HTMLFormatter,
)

# Prompts
from debatedores.prompts import (
    PromptTemplate,
    PromptLibrary,
)

# Config
from debatedores.config import (
    FrameworkConfig,
    DebateSettings,
    LLMSettings,
    EmbeddingSettings,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    "__license__",

    # Core models
    "AgentPerspective",
    "DebateRound",
    "DebateState",
    "FinalResult",

    # Providers
    "LLMProvider",
    "OpenAIProvider",
    "GeminiProvider",

    # Processors
    "DocumentProcessor",
    "PDFProcessor",
    "MarkdownProcessor",
    "WebProcessor",

    # Metrics
    "DebateMetric",
    "AgreementScore",
    "SemanticSimilarity",
    "MetricsAggregator",

    # Agents
    "AgentConfig",
    "Agent",
    "ADVOCATUS_CONFIG",
    "DIABOLI_CONFIG",

    # Stopping
    "StoppingCriterion",
    "AgreementThreshold",
    "MaxRounds",
    "StoppingManager",

    # Strategies
    "DebateStrategy",
    "AdversarialDebate",

    # Formatters
    "OutputFormatter",
    "JSONFormatter",
    "MarkdownFormatter",
    "HTMLFormatter",

    # Prompts
    "PromptTemplate",
    "PromptLibrary",

    # Config
    "FrameworkConfig",
    "DebateSettings",
    "LLMSettings",
    "EmbeddingSettings",
]
