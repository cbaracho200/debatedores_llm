"""
Formatador HTML para resultados de debate.
"""
from debatedores.core.models import FinalResult
from debatedores.formatters.base import OutputFormatter


class HTMLFormatter(OutputFormatter):
    """
    Formata resultados em HTML.

    Gera um documento HTML estilizado e responsivo.
    """

    def format(self, result: FinalResult) -> str:
        """
        Formata resultado como HTML.

        Args:
            result: Resultado final do debate

        Returns:
            String HTML formatada
        """
        status_class = "success" if result.success else "failure"
        status_text = "✅ Sucesso" if result.success else "❌ Falha"

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado do Debate</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .status {{ font-size: 18px; margin: 20px 0; }}
        .status.success {{ color: #28a745; }}
        .status.failure {{ color: #dc3545; }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .metric {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        .metric-label {{ font-size: 14px; color: #666; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .final-answer {{
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .takeaways {{
            list-style: none;
            padding: 0;
        }}
        .takeaways li {{
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        .summary {{
            color: #555;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Resultado do Debate</h1>

        <div class="status {status_class}">
            <strong>Status:</strong> {status_text}
        </div>

        <h2>📊 Métricas</h2>
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Rodadas</div>
                <div class="metric-value">{result.total_rounds}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Agreement Score</div>
                <div class="metric-value">{result.final_agreement_score:.0%}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Tempo (s)</div>
                <div class="metric-value">{result.processing_time:.2f}</div>
            </div>
        </div>

        <h2>💡 Resposta Final</h2>
        <div class="final-answer">
            {self._escape_html(result.final_answer)}
        </div>

        <h2>🔑 Principais Conclusões</h2>
        <ul class="takeaways">
"""

        for takeaway in result.key_takeaways:
            html += f"            <li>{self._escape_html(takeaway)}</li>\n"

        html += f"""        </ul>

        <h2>📝 Resumo do Debate</h2>
        <div class="summary">
            {self._escape_html(result.debate_summary)}
        </div>
    </div>
</body>
</html>"""

        return html

    def _escape_html(self, text: str) -> str:
        """Escapa caracteres HTML especiais."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )


__all__ = ["HTMLFormatter"]
