"""
Classe Agent para execução de debates.
"""
from typing import Optional
from llama_index.core.llms import LLM
from llama_index.core.query_engine import BaseQueryEngine
from debatedores.agents.config import AgentConfig
from debatedores.core.models import AgentPerspective


class Agent:
    """
    Agente de debate que utiliza LLM para gerar perspectivas.

    Um agente combina configuração (nome, role, prompts) com
    capacidades de LLM para participar de debates.
    """

    def __init__(self, config: AgentConfig, llm: LLM):
        """
        Inicializa o agente.

        Args:
            config: Configuração do agente
            llm: Modelo de linguagem para geração
        """
        self.config = config
        self.llm = llm

    async def respond(
        self,
        context: str,
        query_engine: Optional[BaseQueryEngine] = None
    ) -> AgentPerspective:
        """
        Gera resposta do agente dado um contexto.

        Args:
            context: Contexto do debate (pergunta, histórico, etc.)
            query_engine: Engine opcional para consultar documentos

        Returns:
            Perspectiva estruturada do agente
        """
        # Construir prompt completo
        full_prompt = self._build_prompt(context, query_engine)

        # Gerar resposta do LLM
        response = await self.llm.acomplete(full_prompt)

        # Parsear resposta em AgentPerspective
        # Nota: Implementação simplificada - idealmente usar structured output
        return self._parse_response(str(response))

    def _build_prompt(
        self,
        context: str,
        query_engine: Optional[BaseQueryEngine]
    ) -> str:
        """
        Constrói o prompt completo para o agente.

        Args:
            context: Contexto do debate
            query_engine: Engine opcional para documentos

        Returns:
            Prompt formatado
        """
        prompt_parts = [
            self.config.system_prompt,
            "",
            "CONTEXTO DO DEBATE:",
            context,
        ]

        if query_engine is not None:
            prompt_parts.append(
                "\nVocê tem acesso a documentos que podem ser consultados "
                "para fundamentar seus argumentos."
            )

        prompt_parts.append(
            "\nResponda agora com sua análise estruturada."
        )

        return "\n".join(prompt_parts)

    def _parse_response(self, response: str) -> AgentPerspective:
        """
        Parseia resposta do LLM em AgentPerspective.

        Implementação simplificada - idealmente usar structured output.

        Args:
            response: Resposta bruta do LLM

        Returns:
            AgentPerspective estruturada
        """
        # Implementação básica - extrair informações da resposta
        # TODO: Usar Pydantic structured output do LlamaIndex

        return AgentPerspective(
            agent_name=self.config.name,
            position=self._extract_position(response),
            arguments=self._extract_arguments(response),
            confidence=self._extract_confidence(response),
            citations=self._extract_citations(response),
        )

    def _extract_position(self, response: str) -> str:
        """Extrai posição principal da resposta."""
        lines = response.strip().split('\n')
        # Heurística simples: primeira linha significativa
        for line in lines:
            if len(line.strip()) > 20:
                return line.strip()
        return response[:200]

    def _extract_arguments(self, response: str) -> list[str]:
        """Extrai argumentos da resposta."""
        # Heurística: linhas que começam com números ou bullets
        arguments = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                arguments.append(line.lstrip('0123456789.-•) '))
        return arguments[:5] if arguments else [response[:100]]

    def _extract_confidence(self, response: str) -> float:
        """Extrai nível de confiança da resposta."""
        # Buscar por padrões como "confiança: 0.8" ou "confidence: 0.8"
        import re
        pattern = r'confian[çc]a:\s*(0?\.\d+|1\.0)'
        match = re.search(pattern, response.lower())
        if match:
            return float(match.group(1))
        return 0.7  # Default

    def _extract_citations(self, response: str) -> list[str]:
        """Extrai citações da resposta."""
        # Buscar por padrões de citação
        import re
        citations = []
        # Padrão: texto entre aspas
        quoted = re.findall(r'"([^"]+)"', response)
        citations.extend(quoted[:3])
        return citations

    @property
    def name(self) -> str:
        """Retorna o nome do agente."""
        return self.config.name

    @property
    def role(self) -> str:
        """Retorna o papel do agente."""
        return self.config.role


__all__ = ["Agent"]
