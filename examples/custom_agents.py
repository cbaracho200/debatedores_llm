"""
Exemplo com agentes customizados.

Demonstra como criar agentes com configurações personalizadas
para diferentes tipos de debates.
"""
import asyncio
from debatedores.providers import GeminiProvider
from debatedores.agents import Agent, AgentConfig
from debatedores.strategies import AdversarialDebate


async def main():
    """Executa debate com agentes customizados."""

    # 1. Configurar provider (usando Gemini neste exemplo)
    provider = GeminiProvider()
    llm = provider.get_llm()

    # 2. Criar configurações customizadas
    optimist_config = AgentConfig(
        name="Agent Optimista",
        role="optimist",
        system_prompt="""Você é um analista otimista e pragmático.
Foca nos benefícios, oportunidades e aspectos positivos.
Mantenha objetividade mas destaque possibilidades de sucesso.""",
        temperature=0.8,  # Mais criativo
    )

    realist_config = AgentConfig(
        name="Agent Realista",
        role="realist",
        system_prompt="""Você é um analista realista e equilibrado.
Avalia tanto aspectos positivos quanto negativos.
Foca em evidências concretas e análise balanceada.""",
        temperature=0.5,  # Mais conservador
    )

    # 3. Criar agentes
    agents = [
        Agent(optimist_config, llm),
        Agent(realist_config, llm)
    ]

    # 4. Executar debate
    strategy = AdversarialDebate()

    question = "Carros autônomos serão amplamente adotados nos próximos 10 anos?"
    context = f"""
PERGUNTA: {question}

Considere:
- Evolução tecnológica atual
- Desafios regulatórios
- Aceitação social
- Infraestrutura necessária
- Impactos econômicos
"""

    print("🎯 Debate: Optimista vs Realista")
    print(f"Pergunta: {question}\n")

    debate_round = await strategy.execute_round(
        round_number=1,
        agents=agents,
        context=context
    )

    # 5. Exibir perspectivas
    print("\n😊 PERSPECTIVA OTIMISTA")
    print("-" * 60)
    print(f"Posição: {debate_round.agent1_response.position}")
    print(f"Confiança: {debate_round.agent1_response.confidence:.0%}")
    print("\nArgumentos:")
    for i, arg in enumerate(debate_round.agent1_response.arguments, 1):
        print(f"{i}. {arg}")

    print("\n⚖️ PERSPECTIVA REALISTA")
    print("-" * 60)
    print(f"Posição: {debate_round.agent2_response.position}")
    print(f"Confiança: {debate_round.agent2_response.confidence:.0%}")
    print("\nArgumentos:")
    for i, arg in enumerate(debate_round.agent2_response.arguments, 1):
        print(f"{i}. {arg}")

    print(f"\n📊 Convergência: {debate_round.agreement_score:.0%}")


if __name__ == "__main__":
    asyncio.run(main())
