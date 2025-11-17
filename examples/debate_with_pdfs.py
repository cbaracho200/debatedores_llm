"""
Exemplo de debate com documentos PDF.

Demonstra como incluir PDFs no debate para fundamentar
as perspectivas dos agentes.
"""
import asyncio
from pathlib import Path
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from debatedores.providers import OpenAIProvider
from debatedores.processors import PDFProcessor
from debatedores.agents import Agent, ADVOCATUS_CONFIG, DIABOLI_CONFIG
from debatedores.strategies import AdversarialDebate


async def main():
    """Executa debate com PDFs."""

    # 1. Configurar provider
    provider = OpenAIProvider()
    llm = provider.get_llm()
    embed_model = provider.get_embeddings()

    # Configurar LlamaIndex
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50

    # 2. Processar PDFs
    processor = PDFProcessor()
    pdf_paths = [
        "documentos/paper1.pdf",
        "documentos/paper2.pdf"
    ]

    print("📄 Processando documentos...")

    query_tools = []
    for pdf_path in pdf_paths:
        # Verificar se arquivo existe
        if not Path(pdf_path).exists():
            print(f"⚠️ Arquivo não encontrado: {pdf_path}")
            continue

        # Processar PDF
        documents = await processor.process(pdf_path)

        # Criar índice
        index = VectorStoreIndex.from_documents(documents)

        # Criar query engine
        query_engine = index.as_query_engine()

        # Criar tool
        tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name=Path(pdf_path).stem,
            description=f"Documento: {Path(pdf_path).name}"
        )
        query_tools.append(tool)

    # Criar router
    query_engine = RouterQueryEngine.from_defaults(
        query_engine_tools=query_tools
    ) if query_tools else None

    print(f"✅ {len(query_tools)} documentos processados\n")

    # 3. Criar agentes
    agents = [
        Agent(ADVOCATUS_CONFIG, llm),
        Agent(DIABOLI_CONFIG, llm)
    ]

    # 4. Executar debate
    strategy = AdversarialDebate()

    question = "Qual a melhor abordagem para aprendizado de máquina?"
    context = f"""
PERGUNTA: {question}

Analise os documentos fornecidos e construa argumentos
fundamentados nas evidências disponíveis.
"""

    print("🎯 Executando debate com documentos...")

    debate_round = await strategy.execute_round(
        round_number=1,
        agents=agents,
        context=context,
        query_engine=query_engine
    )

    # 5. Exibir resultados
    print("\n📊 RESULTADOS")
    print("=" * 60)
    print(f"\nAgreement Score: {debate_round.agreement_score:.0%}")

    print(f"\n{debate_round.agent1_response.agent_name}:")
    for i, arg in enumerate(debate_round.agent1_response.arguments, 1):
        print(f"  {i}. {arg}")

    print(f"\n{debate_round.agent2_response.agent_name}:")
    for i, arg in enumerate(debate_round.agent2_response.arguments, 1):
        print(f"  {i}. {arg}")


if __name__ == "__main__":
    asyncio.run(main())
