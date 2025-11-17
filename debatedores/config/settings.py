"""
Configurações globais do framework Debatedores.
"""
from typing import Optional
from pydantic import BaseModel, Field


class DebateSettings(BaseModel):
    """
    Configurações para um debate.

    Attributes:
        max_rounds: Número máximo de rodadas
        agreement_target: Meta de convergência (0.0 a 1.0)
        chunk_size: Tamanho dos chunks de documento
        chunk_overlap: Sobreposição entre chunks
        temperature: Temperatura padrão para LLMs
        verbose: Se deve exibir logs detalhados
    """
    max_rounds: int = Field(default=5, ge=1, le=20)
    agreement_target: float = Field(default=0.8, ge=0.0, le=1.0)
    chunk_size: int = Field(default=512, ge=128, le=2048)
    chunk_overlap: int = Field(default=50, ge=0, le=512)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    verbose: bool = Field(default=True)


class LLMSettings(BaseModel):
    """
    Configurações de LLM.

    Attributes:
        provider: Provider de LLM ("openai", "gemini", etc.)
        model_name: Nome do modelo
        api_key: API key (opcional, usa env var se None)
        max_tokens: Limite de tokens
        timeout: Timeout em segundos
    """
    provider: str = Field(default="openai")
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    max_tokens: Optional[int] = None
    timeout: int = Field(default=300)


class EmbeddingSettings(BaseModel):
    """
    Configurações de embeddings.

    Attributes:
        provider: Provider de embeddings
        model_name: Nome do modelo
        api_key: API key (opcional)
    """
    provider: str = Field(default="openai")
    model_name: Optional[str] = None
    api_key: Optional[str] = None


class FrameworkConfig(BaseModel):
    """
    Configuração completa do framework.

    Attributes:
        debate: Configurações de debate
        llm: Configurações de LLM
        embedding: Configurações de embeddings
    """
    debate: DebateSettings = Field(default_factory=DebateSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)

    @classmethod
    def from_yaml(cls, path: str) -> "FrameworkConfig":
        """
        Carrega configuração de arquivo YAML.

        Args:
            path: Caminho para o arquivo YAML

        Returns:
            Configuração carregada
        """
        import yaml
        from pathlib import Path

        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def to_yaml(self, path: str) -> None:
        """
        Salva configuração em arquivo YAML.

        Args:
            path: Caminho para salvar o arquivo
        """
        import yaml
        from pathlib import Path

        config_path = Path(path)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                self.model_dump(),
                f,
                default_flow_style=False,
                allow_unicode=True
            )


__all__ = [
    "DebateSettings",
    "LLMSettings",
    "EmbeddingSettings",
    "FrameworkConfig",
]
