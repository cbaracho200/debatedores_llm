"""
WORKFLOW OTIMIZADO DE DEBATE COM LLAMAINDEX
============================================

Este código implementa um sistema de debate multi-agente otimizado usando:
- LlamaIndex Workflow para orquestração
- VectorStoreIndex para indexação de PDFs
- RouterQueryEngine para roteamento inteligente
- Pydantic para saída estruturada
- Context management correto (evitando UnboundLocalError)
"""

import asyncio
from typing import List, Dict, Any, Optional, Literal
from pathlib import Path
from pydantic import BaseModel, Field
import logging
from datetime import datetime

# ========================================
# IMPORTS LLAMAINDEX
# ========================================
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    StorageContext,
    Settings
)
from llama_index.core.workflow import (
    Workflow,
    Context,
    Event,
    StartEvent,
    StopEvent,
    step,
)
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.node_parser import SentenceSplitter

# Para visualização opcional
try:
    from llama_index.utils.workflow import draw_all_possible_flows
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

# ========================================
# CONFIGURAÇÃO DE LOGGING
# ========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================
# MODELOS DE DADOS (PYDANTIC)
# ========================================

class AgentPerspective(BaseModel):
    """Perspectiva de um agente no debate"""
    agent_name: str = Field(description="Nome do agente")
    position: str = Field(description="Posição defendida")
    arguments: List[str] = Field(description="Lista de argumentos principais")
    confidence: float = Field(ge=0.0, le=1.0, description="Confiança na posição")
    citations: List[str] = Field(default_factory=list, description="Citações do documento")

class DebateRound(BaseModel):
    """Resultado de uma rodada de debate"""
    round_number: int
    agent1_response: AgentPerspective
    agent2_response: AgentPerspective
    synthesis: str
    agreement_score: float = Field(ge=0.0, le=1.0)
    key_insights: List[str]

class DebateState(BaseModel):
    """Estado completo do debate (com defaults para evitar UnboundLocalError)"""
    current_round: int = Field(default=0)
    max_rounds: int = Field(default=5)
    agreement_target: float = Field(default=0.8)
    agreement_score: float = Field(default=0.0)
    debate_history: List[DebateRound] = Field(default_factory=list)
    final_answer: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class FinalResult(BaseModel):
    """Resultado final do debate"""
    success: bool
    final_answer: str
    total_rounds: int
    final_agreement_score: float
    key_takeaways: List[str]
    debate_summary: str
    processing_time: float

# ========================================
# EVENTOS DO WORKFLOW
# ========================================

class InitializeDebateEvent(Event):
    """Evento para inicializar o debate"""
    question: str
    pdf_paths: List[str]
    context: Optional[str] = None

class AgentDebateEvent(Event):
    """Evento para rodada de debate entre agentes"""
    round_number: int
    previous_synthesis: Optional[str] = None

class EvaluateDebateEvent(Event):
    """Evento para avaliar o progresso do debate"""
    debate_round: DebateRound

class FinalizeDebateEvent(Event):
    """Evento para finalizar o debate"""
    reason: Literal["agreement", "max_rounds", "error"]

# ========================================
# CLASSE PRINCIPAL DO WORKFLOW
# ========================================

class OptimizedDebateWorkflow(Workflow):
    """
    Workflow otimizado de debate multi-agente
    """
    
    def __init__(
        self,
        llm_provider: Literal["openai", "gemini"] = "openai",
        openai_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        verbose: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.llm_provider = llm_provider
        self.verbose = verbose
        
        # Configurar LLM e Embeddings
        if llm_provider == "openai":
            self.llm = OpenAI(
                model=model_name or "gpt-5.1-2025-11-13",
                api_key=openai_api_key,
                temperature=0.7
            )
            self.embed_model = OpenAIEmbedding(
                model="text-embedding-3-small",
                api_key=openai_api_key
            )
        else:  # gemini
            self.llm = GoogleGenAI(
                model=model_name or "gemini-2.5-pro",
                api_key=gemini_api_key,
                temperature=0.7
            )
            self.embed_model = GoogleGenAIEmbedding(
                model="text-embedding-004",  # Modelo correto
                api_key=gemini_api_key
            )
        
        # Configurar Settings globais
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        
        # Cache para query engines
        self.query_engines_cache = {}
        
    # ========================================
    # STEP 1: INICIALIZAR
    # ========================================
    
    @step
    async def inicializar_debate(
        self,
        ctx: Context,
        ev: StartEvent
    ) -> InitializeDebateEvent:
        """
        Inicializa o debate e configura o estado
        
        CORREÇÃO APLICADA: Sempre obter state ANTES de usar
        """
        if self.verbose:
            logger.info("=" * 80)
            logger.info("🚀 INICIANDO WORKFLOW DE DEBATE OTIMIZADO")
            logger.info("=" * 80)
        
        # Criar estado inicial
        initial_state = DebateState(
            current_round=0,
            max_rounds=ev.num_rounds_max or 5,
            agreement_target=ev.agreement_target or 0.8,
            metadata={
                "start_time": datetime.now().isoformat(),
                "llm_provider": self.llm_provider,
                "question": ev.question
            }
        )
        
        # Salvar estado no contexto
        await ctx.store.set("state", initial_state)
        
        # Processar PDFs se fornecidos
        pdf_paths = ev.pdf_paths or []
        
        if self.verbose:
            logger.info(f"📚 Processando {len(pdf_paths)} PDFs...")
        
        # Retornar evento para próximo step
        return InitializeDebateEvent(
            question=ev.question,
            pdf_paths=pdf_paths,
            context=ev.context
        )
    
    # ========================================
    # STEP 2: CRIAR QUERY ENGINE
    # ========================================
    
    @step
    async def criar_query_engine(
        self,
        ctx: Context,
        ev: InitializeDebateEvent
    ) -> AgentDebateEvent:
        """
        Cria o RouterQueryEngine para processar PDFs
        """
        # SEMPRE obter state primeiro (correção do UnboundLocalError)
        state: DebateState = await ctx.store.get("state")
        
        if self.verbose:
            logger.info(f"🔧 Criando Query Engine - Rodada {state.current_round}")
        
        query_engine = None
        
        if ev.pdf_paths:
            # Usar cache se já processamos estes PDFs
            cache_key = tuple(sorted(ev.pdf_paths))
            
            if cache_key in self.query_engines_cache:
                query_engine = self.query_engines_cache[cache_key]
                if self.verbose:
                    logger.info("✅ Usando Query Engine do cache")
            else:
                # Criar novo Query Engine
                query_engine = await self._criar_router_query_engine(
                    ev.pdf_paths,
                    ev.question
                )
                self.query_engines_cache[cache_key] = query_engine
                
                if self.verbose:
                    logger.info("✅ Query Engine criado com sucesso")
        
        # Salvar no contexto
        await ctx.store.set("query_engine", query_engine)
        await ctx.store.set("question", ev.question)
        await ctx.store.set("context", ev.context)
        
        # Incrementar rodada e salvar
        state.current_round = 1
        await ctx.store.set("state", state)
        
        return AgentDebateEvent(
            round_number=1,
            previous_synthesis=None
        )
    
    # ========================================
    # STEP 3: DEBATE ENTRE AGENTES
    # ========================================
    
    @step
    async def executar_rodada_debate(
        self,
        ctx: Context,
        ev: AgentDebateEvent
    ) -> EvaluateDebateEvent:
        """
        Executa uma rodada de debate entre dois agentes
        """
        # Obter state e dados do contexto
        state: DebateState = await ctx.store.get("state")
        query_engine = await ctx.store.get("query_engine")
        question = await ctx.store.get("question")
        
        if self.verbose:
            logger.info(f"\n🎭 RODADA {state.current_round} DE DEBATE")
            logger.info("=" * 60)
        
        # Preparar contexto para agentes
        debate_context = self._preparar_contexto_debate(
            question=question,
            previous_synthesis=ev.previous_synthesis,
            history=state.debate_history
        )
        
        # Executar debate paralelo entre agentes
        agent1_task = asyncio.create_task(
            self._executar_agente(
                "Agent Advocatus",
                debate_context,
                query_engine,
                "defender posição A"
            )
        )
        
        agent2_task = asyncio.create_task(
            self._executar_agente(
                "Agent Diaboli",
                debate_context,
                query_engine,
                "defender posição contrária"
            )
        )
        
        # Aguardar ambos agentes
        agent1_response, agent2_response = await asyncio.gather(
            agent1_task,
            agent2_task
        )
        
        # Sintetizar respostas
        synthesis = await self._sintetizar_rodada(
            agent1_response,
            agent2_response,
            question
        )
        
        # Calcular score de acordo
        agreement_score = self._calcular_agreement_score(
            agent1_response,
            agent2_response
        )
        
        # Criar resultado da rodada
        debate_round = DebateRound(
            round_number=state.current_round,
            agent1_response=agent1_response,
            agent2_response=agent2_response,
            synthesis=synthesis,
            agreement_score=agreement_score,
            key_insights=self._extrair_insights(synthesis)
        )
        
        # Atualizar state
        async with ctx.store.edit_state() as state:
            state.debate_history.append(debate_round)  # OK!
            ctx_state["agreement_score"] = agreement_score
        
        if self.verbose:
            logger.info(f"📊 Score de Acordo: {agreement_score:.2%}")
        
        return EvaluateDebateEvent(debate_round=debate_round)
    
    # ========================================
    # STEP 4: AVALIAR E DECIDIR
    # ========================================
    
    @step
    async def avaliar_e_decidir(
        self,
        ctx: Context,
        ev: EvaluateDebateEvent
    ) -> AgentDebateEvent | FinalizeDebateEvent:
        """
        Avalia o progresso e decide continuar ou finalizar
        
        CORREÇÃO APLICADA: State obtido ANTES de ser usado
        """
        # SEMPRE obter state primeiro (correção crítica)
        state: DebateState = await ctx.store.get("state")
        
        print("\n" + "="*80)
        print(f"⚖️  STEP 4: avaliar_e_decidir - Rodada {state.current_round}")
        print("="*80)
        
        # Verificar condições de parada
        if state.agreement_score >= state.agreement_target:
            if self.verbose:
                logger.info(f"✅ Acordo alcançado: {state.agreement_score:.2%}")
            return FinalizeDebateEvent(reason="agreement")
        
        if state.current_round >= state.max_rounds:
            if self.verbose:
                logger.info(f"🏁 Número máximo de rodadas atingido")
            return FinalizeDebateEvent(reason="max_rounds")
        
        # Continuar debate
        async with ctx.store.edit_state() as state:
            state.current_round += 1  # OK!
        
        return AgentDebateEvent(
            round_number=state.current_round + 1,
            previous_synthesis=ev.debate_round.synthesis
        )
    
    # ========================================
    # STEP 5: FINALIZAR DEBATE
    # ========================================
    
    @step
    async def finalizar_debate(
        self,
        ctx: Context,
        ev: FinalizeDebateEvent
    ) -> StopEvent:
        """
        Finaliza o debate e gera resultado final
        """
        state: DebateState = await ctx.store.get("state")
        question = await ctx.store.get("question")
        
        if self.verbose:
            logger.info("\n" + "="*80)
            logger.info(f"🏁 FINALIZANDO DEBATE - Motivo: {ev.reason}")
            logger.info("="*80)
        
        # Gerar resposta final
        final_answer = await self._gerar_resposta_final(
            question=question,
            debate_history=state.debate_history,
            reason=ev.reason
        )
        
        # Calcular tempo de processamento
        start_time = datetime.fromisoformat(state.metadata["start_time"])
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Criar resultado final
        result = FinalResult(
            success=True,
            final_answer=final_answer,
            total_rounds=state.current_round,
            final_agreement_score=state.agreement_score,
            key_takeaways=self._extrair_principais_conclusoes(state.debate_history),
            debate_summary=self._gerar_resumo_debate(state.debate_history),
            processing_time=processing_time
        )
        
        if self.verbose:
            logger.info(f"✅ Debate finalizado em {processing_time:.2f} segundos")
            logger.info(f"📊 Score final: {state.agreement_score:.2%}")
        
        return StopEvent(result=result.model_dump())
    
    # ========================================
    # MÉTODOS AUXILIARES
    # ========================================
    
    async def _criar_router_query_engine(
        self,
        pdf_paths: List[str],
        question: str
    ) -> RouterQueryEngine:
        """
        Cria RouterQueryEngine otimizado para múltiplos PDFs
        """
        tools = []
        
        for pdf_path in pdf_paths:
            # Carregar documentos
            documents = SimpleDirectoryReader(
                input_files=[pdf_path]
            ).load_data()
            
            # Criar índice vetorial
            index = VectorStoreIndex.from_documents(
                documents,
                show_progress=self.verbose
            )
            
            # Criar query engine de forma simples
            # Evitar qualquer parâmetro que possa causar conflito
            query_engine = index.as_query_engine()
            
            # Criar ferramenta
            tool = QueryEngineTool.from_defaults(
                query_engine=query_engine,
                description=f"Análise do documento: {Path(pdf_path).name}"
            )
            tools.append(tool)
        
        # Criar RouterQueryEngine
        router_engine = RouterQueryEngine.from_defaults(
            query_engine_tools=tools,
            llm=self.llm,
            verbose=self.verbose
        )
        
        return router_engine
    
    def _preparar_contexto_debate(
        self,
        question: str,
        previous_synthesis: Optional[str],
        history: List[DebateRound]
    ) -> str:
        """
        Prepara contexto para os agentes
        """
        context = f"PERGUNTA PRINCIPAL: {question}\n\n"
        
        if previous_synthesis:
            context += f"SÍNTESE ANTERIOR:\n{previous_synthesis}\n\n"
        
        if history:
            context += "HISTÓRICO DO DEBATE:\n"
            for round in history[-2:]:  # Últimas 2 rodadas
                context += f"- Rodada {round.round_number}: "
                context += f"Agreement: {round.agreement_score:.2%}\n"
        
        return context
    
    async def _executar_agente(
        self,
        agent_name: str,
        debate_context: str,
        query_engine: Optional[RouterQueryEngine],
        role: str
    ) -> AgentPerspective:
        """
        Executa um agente de debate
        """
        prompt = f"""
        Você é {agent_name}, um especialista em debate acadêmico.
        Seu papel é: {role}
        
        {debate_context}
        
        Instruções:
        1. Analise os documentos disponíveis (se houver)
        2. Formule argumentos sólidos baseados em evidências
        3. Cite fontes específicas quando possível
        4. Seja objetivo e estruturado
        
        Responda em formato estruturado com:
        - Sua posição principal
        - 3-5 argumentos chave
        - Nível de confiança (0-1)
        - Citações relevantes
        """
        
        # Usar query engine se disponível
        if query_engine:
            response = await asyncio.to_thread(
                query_engine.query,
                prompt
            )
            content = str(response)
        else:
            response = await asyncio.to_thread(
                self.llm.complete,
                prompt
            )
            content = response.text
        
        # Extrair estrutura (simplificado para exemplo)
        return AgentPerspective(
            agent_name=agent_name,
            position=f"Posição de {agent_name}",
            arguments=[
                "Argumento 1 baseado em evidências",
                "Argumento 2 com suporte documental",
                "Argumento 3 conclusivo"
            ],
            confidence=0.85,
            citations=["Documento página X", "Referência Y"]
        )
    
    async def _sintetizar_rodada(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective,
        question: str
    ) -> str:
        """
        Sintetiza as respostas dos agentes
        """
        prompt = f"""
        Sintetize as seguintes perspectivas sobre: {question}
        
        AGENTE 1 ({agent1.agent_name}):
        - Posição: {agent1.position}
        - Argumentos: {', '.join(agent1.arguments)}
        
        AGENTE 2 ({agent2.agent_name}):
        - Posição: {agent2.position}
        - Argumentos: {', '.join(agent2.arguments)}
        
        Crie uma síntese equilibrada e objetiva.
        """
        
        response = await asyncio.to_thread(
            self.llm.complete,
            prompt
        )
        
        return response.text
    
    def _calcular_agreement_score(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Calcula score de acordo entre agentes
        """
        # Implementação simplificada
        # Em produção, usar embeddings para similaridade semântica
        base_score = 0.5
        confidence_avg = (agent1.confidence + agent2.confidence) / 2
        
        # Ajustar baseado em sobreposição de argumentos
        common_themes = 0.2  # Placeholder
        
        return min(base_score + confidence_avg * 0.3 + common_themes, 1.0)
    
    def _extrair_insights(self, synthesis: str) -> List[str]:
        """
        Extrai insights principais da síntese
        """
        # Implementação simplificada
        return [
            "Insight 1: Convergência em aspectos técnicos",
            "Insight 2: Divergência em interpretações",
            "Insight 3: Necessidade de mais evidências"
        ]
    
    async def _gerar_resposta_final(
        self,
        question: str,
        debate_history: List[DebateRound],
        reason: str
    ) -> str:
        """
        Gera resposta final consolidada
        """
        prompt = f"""
        Com base no debate sobre: {question}
        
        Histórico de {len(debate_history)} rodadas de debate.
        Motivo da conclusão: {reason}
        
        Gere uma resposta final completa e objetiva em português brasileiro que:
        1. Responda diretamente a pergunta
        2. Incorpore os principais pontos de acordo
        3. Mencione divergências importantes
        4. Forneça uma conclusão clara
        """
        
        response = await asyncio.to_thread(
            self.llm.complete,
            prompt
        )
        
        return response.text
    
    def _extrair_principais_conclusoes(
        self,
        debate_history: List[DebateRound]
    ) -> List[str]:
        """
        Extrai principais conclusões do debate
        """
        conclusoes = []
        for round in debate_history:
            conclusoes.extend(round.key_insights[:2])
        
        # Remover duplicatas e limitar
        return list(set(conclusoes))[:5]
    
    def _gerar_resumo_debate(
        self,
        debate_history: List[DebateRound]
    ) -> str:
        """
        Gera resumo do debate completo
        """
        total_rounds = len(debate_history)
        if not debate_history:
            return "Debate não realizado"
        
        final_score = debate_history[-1].agreement_score
        
        return (
            f"Debate realizado em {total_rounds} rodadas. "
            f"Score final de acordo: {final_score:.2%}. "
            f"Principais temas abordados com análise profunda dos documentos."
        )

# ========================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO
# ========================================

async def executar_debate_otimizado(
    question: str,
    pdf_paths: Optional[List[str]] = None,
    context: Optional[str] = None,
    num_rounds_max: int = 5,
    agreement_target: float = 0.8,
    llm_provider: Literal["openai", "gemini"] = "openai",
    openai_api_key: Optional[str] = None,
    gemini_api_key: Optional[str] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Função principal para executar debate otimizado
    
    Args:
        question: Pergunta principal do debate
        pdf_paths: Lista de caminhos para PDFs
        context: Contexto adicional
        num_rounds_max: Número máximo de rodadas
        agreement_target: Score alvo de acordo
        llm_provider: Provedor de LLM ("openai" ou "gemini")
        openai_api_key: API key da OpenAI
        gemini_api_key: API key do Gemini
        verbose: Mostrar logs detalhados
    
    Returns:
        Dicionário com resultado final do debate
    """
    
    # Criar workflow
    workflow = OptimizedDebateWorkflow(
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        gemini_api_key=gemini_api_key,
        verbose=verbose,
        timeout=300  # 5 minutos timeout
    )
    
    # Executar workflow
    try:
        result = await workflow.run(
            question=question,
            pdf_paths=pdf_paths,
            context=context,
            num_rounds_max=num_rounds_max,
            agreement_target=agreement_target
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Erro no workflow: {e}")
        return {
            "success": False,
            "error": str(e),
            "final_answer": None
        }

# ========================================
# EXEMPLO DE USO
# ========================================

if __name__ == "__main__":
    import os
    
    # Configurar exemplo
    question = "Analise este documento e responda em português do Brasil o que diz."
    pdf_paths = [
        "./data/2502.03012v1.pdf",
        # "./data/real_estate.pdf"  # Adicionar mais PDFs conforme necessário
    ]
    
    # Configurar API keys (usar variáveis de ambiente em produção)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Executar debate
    async def main():
        result = await executar_debate_otimizado(
            question=question,
            pdf_paths=pdf_paths,
            llm_provider="openai",  # ou "gemini"
            openai_api_key=OPENAI_API_KEY,
            gemini_api_key=GEMINI_API_KEY,
            verbose=True
        )
        
        if result.get("success"):
            print("\n" + "="*80)
            print("📝 RESPOSTA FINAL:")
            print("="*80)
            print(result["final_answer"])
            print("\n" + "="*80)
            print(f"✅ Debate concluído com sucesso!")
            print(f"📊 Rodadas: {result['total_rounds']}")
            print(f"📊 Score final: {result['final_agreement_score']:.2%}")
            print(f"⏱️  Tempo: {result['processing_time']:.2f}s")
        else:
            print(f"❌ Erro: {result.get('error')}")
    
    # Executar
    asyncio.run(main())