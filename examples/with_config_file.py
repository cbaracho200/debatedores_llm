"""
Exemplo usando arquivo de configuração YAML.

Demonstra como carregar configurações de um arquivo
para parametrizar debates.
"""
import asyncio
from debatedores.config import FrameworkConfig
from debatedores.providers import OpenAIProvider, GeminiProvider
from debatedores.agents import Agent, ADVOCATUS_CONFIG, DIABOLI_CONFIG
from debatedores.strategies import AdversarialDebate


async def main():
    """Executa debate usando configuração de arquivo."""

    # 1. Carregar configuração do YAML
    print("📋 Carregando configuração...")

    try:
        config = FrameworkConfig.from_yaml("config.yaml")
    except FileNotFoundError:
        print("⚠️ Arquivo config.yaml não encontrado.")
        print("📝 Usando configuração padrão e salvando exemplo...")

        config = FrameworkConfig()
        config.to_yaml("config.yaml")
        print("✅ Arquivo config.yaml criado com valores padrão\n")

    # 2. Configurar provider baseado no config
    if config.llm.provider == "openai":
        provider = OpenAIProvider(
            api_key=config.llm.api_key,
            default_llm_model=config.llm.model_name
        )
    elif config.llm.provider == "gemini":
        provider = GeminiProvider(
            api_key=config.llm.api_key,
            default_llm_model=config.llm.model_name
        )
    else:
        raise ValueError(f"Provider não suportado: {config.llm.provider}")

    llm = provider.get_llm(temperature=config.debate.temperature)

    print(f"🤖 Provider: {config.llm.provider}")
    print(f"🎯 Max rodadas: {config.debate.max_rounds}")
    print(f"📊 Agreement target: {config.debate.agreement_target:.0%}\n")

    # 3. Criar agentes
    agents = [
        Agent(ADVOCATUS_CONFIG, llm),
        Agent(DIABOLI_CONFIG, llm)
    ]

    # 4. Executar debate
    strategy = AdversarialDebate()

    question = "Energia nuclear é solução para mudanças climáticas?"

    debate_round = await strategy.execute_round(
        round_number=1,
        agents=agents,
        context=f"PERGUNTA: {question}"
    )

    # 5. Verificar critério de parada baseado no config
    print(f"📈 Agreement Score: {debate_round.agreement_score:.0%}")

    if debate_round.agreement_score >= config.debate.agreement_target:
        print("✅ Meta de convergência atingida!")
    else:
        print(f"⏳ Convergência atual abaixo da meta "
              f"({config.debate.agreement_target:.0%})")


if __name__ == "__main__":
    asyncio.run(main())
