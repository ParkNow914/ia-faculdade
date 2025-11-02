"""
FUNÇÕES UTILITÁRIAS ADICIONAIS
Utilidades para exportação de dados, análise e relatórios.
"""

import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
import csv
from pathlib import Path


class DataExporter:
    """
    Classe para exportar dados e previsões em múltiplos formatos.
    """
    
    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
        """
        Exporta dados para CSV.
        
        Args:
            data: Lista de dicionários com dados
            filename: Nome do arquivo (sem extensão)
            
        Returns:
            Path do arquivo criado
        """
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"{filename}_{timestamp}.csv"
        
        if not data:
            raise ValueError("No data to export")
        
        # Usar pandas para criar CSV
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        
        return str(filepath)
    
    @staticmethod
    def export_to_json(data: List[Dict[str, Any]], filename: str, pretty: bool = True) -> str:
        """
        Exporta dados para JSON.
        """
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"{filename}_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)
        
        return str(filepath)
    
    @staticmethod
    def export_to_excel(data: List[Dict[str, Any]], filename: str, sheet_name: str = "Data") -> str:
        """
        Exporta dados para Excel.
        """
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"{filename}_{timestamp}.xlsx"
        
        df = pd.DataFrame(data)
        df.to_excel(filepath, sheet_name=sheet_name, index=False)
        
        return str(filepath)
    
    @staticmethod
    def create_prediction_report(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cria relatório estatístico de previsões.
        """
        if not predictions:
            return {"error": "No predictions to analyze"}
        
        df = pd.DataFrame(predictions)
        
        # Assumir que tem coluna 'predicted_consumption_kwh'
        consumption_col = 'predicted_consumption_kwh'
        
        if consumption_col in df.columns:
            report = {
                "total_predictions": len(df),
                "statistics": {
                    "mean": float(df[consumption_col].mean()),
                    "median": float(df[consumption_col].median()),
                    "std": float(df[consumption_col].std()),
                    "min": float(df[consumption_col].min()),
                    "max": float(df[consumption_col].max()),
                    "q25": float(df[consumption_col].quantile(0.25)),
                    "q75": float(df[consumption_col].quantile(0.75))
                },
                "generated_at": datetime.now().isoformat()
            }
            
            return report
        
        return {"error": "Required column not found"}


class DataAnalyzer:
    """
    Análise de dados e detecção de padrões.
    """
    
    @staticmethod
    def detect_outliers(values: List[float], threshold: float = 3.0) -> Dict[str, Any]:
        """
        Detecta outliers usando z-score.
        """
        import numpy as np
        
        if len(values) < 3:
            return {"outliers": [], "count": 0}
        
        values_array = np.array(values)
        mean = np.mean(values_array)
        std = np.std(values_array)
        
        if std == 0:
            return {"outliers": [], "count": 0}
        
        z_scores = np.abs((values_array - mean) / std)
        outlier_indices = np.where(z_scores > threshold)[0].tolist()
        
        outliers = [
            {
                "index": int(idx),
                "value": float(values[idx]),
                "z_score": float(z_scores[idx])
            }
            for idx in outlier_indices
        ]
        
        return {
            "outliers": outliers,
            "count": len(outliers),
            "percentage": (len(outliers) / len(values)) * 100
        }
    
    @staticmethod
    def analyze_time_series(data: pd.DataFrame, value_column: str) -> Dict[str, Any]:
        """
        Analisa série temporal.
        """
        if value_column not in data.columns:
            return {"error": f"Column {value_column} not found"}
        
        values = data[value_column]
        
        analysis = {
            "basic_stats": {
                "count": int(len(values)),
                "mean": float(values.mean()),
                "std": float(values.std()),
                "min": float(values.min()),
                "max": float(values.max())
            },
            "trend": "increasing" if values.iloc[-1] > values.iloc[0] else "decreasing",
            "volatility": float(values.std() / values.mean()) if values.mean() != 0 else 0
        }
        
        return analysis


class ReportGenerator:
    """
    Gerador de relatórios em múltiplos formatos.
    """
    
    @staticmethod
    def generate_html_report(data: Dict[str, Any], title: str = "EnergyFlow AI Report") -> str:
        """
        Gera relatório HTML.
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                .stat {{ background-color: #ecf0f1; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p>Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="content">
        """
        
        # Adicionar dados
        for key, value in data.items():
            html += f"<h2>{key.replace('_', ' ').title()}</h2>"
            
            if isinstance(value, dict):
                html += "<div class='stat'>"
                for k, v in value.items():
                    html += f"<p><strong>{k}:</strong> {v}</p>"
                html += "</div>"
            else:
                html += f"<p>{value}</p>"
        
        html += """
            </div>
        </body>
        </html>
        """
        
        # Salvar
        output_dir = Path("exports/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"report_{timestamp}.html"
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return str(filepath)
