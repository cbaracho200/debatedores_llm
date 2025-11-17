"""
Testes para formatadores de saída.
"""
import json
from debatedores.core.models import FinalResult
from debatedores.formatters import (
    JSONFormatter,
    MarkdownFormatter,
    HTMLFormatter
)


def create_sample_result():
    """Cria resultado de exemplo para testes."""
    return FinalResult(
        success=True,
        final_answer="Resposta final de teste",
        total_rounds=3,
        final_agreement_score=0.85,
        key_takeaways=["Ponto 1", "Ponto 2"],
        debate_summary="Resumo do debate",
        processing_time=10.5
    )


def test_json_formatter():
    """Testa formatador JSON."""
    formatter = JSONFormatter()
    result = create_sample_result()

    output = formatter.format(result)

    # Deve ser JSON válido
    parsed = json.loads(output)

    assert parsed['success'] is True
    assert parsed['total_rounds'] == 3
    assert parsed['final_agreement_score'] == 0.85


def test_json_formatter_to_dict():
    """Testa conversão para dicionário."""
    formatter = JSONFormatter()
    result = create_sample_result()

    output_dict = formatter.format_to_dict(result)

    assert isinstance(output_dict, dict)
    assert output_dict['success'] is True


def test_markdown_formatter():
    """Testa formatador Markdown."""
    formatter = MarkdownFormatter()
    result = create_sample_result()

    output = formatter.format(result)

    # Verificar elementos markdown
    assert "# " in output  # Cabeçalhos
    assert "**" in output  # Negrito
    assert "##" in output  # Subcabeçalhos
    assert "Resposta final de teste" in output
    assert "85%" in output or "0.85" in output


def test_html_formatter():
    """Testa formatador HTML."""
    formatter = HTMLFormatter()
    result = create_sample_result()

    output = formatter.format(result)

    # Verificar elementos HTML
    assert "<!DOCTYPE html>" in output
    assert "<html" in output
    assert "</html>" in output
    assert "Resposta final de teste" in output
    assert "<div" in output
