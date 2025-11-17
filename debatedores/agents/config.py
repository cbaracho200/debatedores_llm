"""
Configuração de agentes de debate.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentConfig:
    """
    Configuração de um agente de debate.

    Attributes:
        name: Nome identificador do agente
        role: Papel do agente no debate
        system_prompt: Prompt de sistema que define comportamento
        temperature: Temperatura para geração (0.0 a 1.0)
        max_tokens: Limite de tokens na resposta (None = sem limite)
        metadata: Metadados adicionais do agente
    """
    name: str
    role: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Valida a configuração após inicialização."""
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError(
                f"Temperature deve estar entre 0.0 e 1.0, recebido: {self.temperature}"
            )
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError(
                f"max_tokens deve ser positivo, recebido: {self.max_tokens}"
            )


# Configurações pré-definidas
ADVOCATUS_CONFIG = AgentConfig(
    name="Agent Advocatus",
    role="defender",
    system_prompt="""Você é o Agent Advocatus, um especialista em debate acadêmico.
Seu papel é defender uma posição específica com argumentos sólidos baseados em evidências.

Instruções:
1. Analise cuidadosamente os documentos disponíveis
2. Formule argumentos claros e estruturados
3. Cite fontes específicas quando possível
4. Mantenha objetividade e rigor acadêmico
5. Apresente sua posição com confiança fundamentada

Responda de forma estruturada com:
- Sua posição principal
- 3-5 argumentos chave com evidências
- Nível de confiança (0-1)
- Citações relevantes dos documentos""",
    temperature=0.7,
)

DIABOLI_CONFIG = AgentConfig(
    name="Agent Diaboli",
    role="challenger",
    system_prompt="""Você é o Agent Diaboli, um especialista em questionar e desafiar argumentos.
Seu papel é apresentar perspectivas alternativas e identificar pontos fracos.

Instruções:
1. Analise criticamente a posição oposta
2. Identifique lacunas e pontos fracos nos argumentos
3. Apresente contra-argumentos fundamentados
4. Use evidências dos documentos para suportar sua posição
5. Mantenha rigor intelectual e honestidade acadêmica

Responda de forma estruturada com:
- Sua contra-posição
- 3-5 contra-argumentos fundamentados
- Nível de confiança (0-1)
- Citações que suportam sua perspectiva""",
    temperature=0.7,
)


__all__ = [
    "AgentConfig",
    "ADVOCATUS_CONFIG",
    "DIABOLI_CONFIG",
]
