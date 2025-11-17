"""
Exemplo básico de uso do framework Debatedores.

Este exemplo demonstra como executar um debate simples
usando configurações padrão.
"""
import asyncio
from debatedores.providers import OpenAIProvider
from debatedores.agents import Agent, ADVOCATUS_CONFIG, DIABOLI_CONFIG
from debatedores.strategies import AdversarialDebate
from debatedores.core.models import DebateState
from debatedores.formatters import MarkdownFormatter


async def main():
    """Executa um debate básico."""

    # 1. Configurar provider
    provider = OpenAIProvider()

    # 2. Obter LLM
    llm = provider.get_llm()

    # 3. Criar agentes
    agents = [
        Agent(ADVOCATUS_CONFIG, llm),
        Agent(DIABOLI_CONFIG, llm)
    ]

    # 4. Configurar estratégia
    strategy = AdversarialDebate()

    # 5. Preparar contexto
    question = "Inteligência Artificial deve ser regulamentada?"
    context = f"""
PERGUNTA: {question}

Considere aspectos como:
- Segurança e ética
- Inovação tecnológica
- Impactos sociais e econômicos
- Precedentes históricos de regulação tecnológica
"""

    # 6. Executar rodada de debate
    print("🎯 Iniciando debate...")
    print(f"Pergunta: {question}\n")

    debate_round = await strategy.execute_round(
        round_number=1,
        agents=agents,
        context=context
    )

    # 7. Exibir resultados
    print("\n📊 RESULTADOS DA RODADA 1")
    print("=" * 60)
    print(f"\n{debate_round.agent1_response.agent_name}:")
    print(f"Posição: {debate_round.agent1_response.position}")
    print(f"Confiança: {debate_round.agent1_response.confidence:.0%}")

    print(f"\n{debate_round.agent2_response.agent_name}:")
    print(f"Posição: {debate_round.agent2_response.position}")
    print(f"Confiança: {debate_round.agent2_response.confidence:.0%}")

    print(f"\n📈 Agreement Score: {debate_round.agreement_score:.0%}")
    print(f"\n📝 Síntese:\n{debate_round.synthesis}")


if __name__ == "__main__":
    # Executar debate
    asyncio.run(main())
