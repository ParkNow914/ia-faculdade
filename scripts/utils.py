"""
SCRIPTS DE UTILIDADES
Scripts auxiliares para manutenção e operações do sistema.
"""

import os
import sys
from pathlib import Path

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def cleanup_logs():
    """Limpa logs antigos (>30 dias)."""
    import time
    
    logs_dir = project_root / "logs"
    if not logs_dir.exists():
        print("📁 Diretório de logs não existe")
        return
    
    cutoff = time.time() - (30 * 24 * 60 * 60)  # 30 dias
    removed_count = 0
    
    for log_file in logs_dir.glob("*.log"):
        if log_file.stat().st_mtime < cutoff:
            log_file.unlink()
            removed_count += 1
            print(f"🗑️ Removido: {log_file.name}")
    
    print(f"\n✅ {removed_count} arquivos de log removidos")


def check_system_health():
    """Verifica saúde do sistema."""
    print("🔍 Verificando saúde do sistema...\n")
    
    checks = []
    
    # Verificar modelo
    model_file = project_root / "src/model/saved_models/regression_model.pkl"
    checks.append(("Modelo treinado", model_file.exists()))
    
    # Verificar scalers
    scaler_features = project_root / "src/model/saved_models/scaler_features.pkl"
    scaler_target = project_root / "src/model/saved_models/scaler_target.pkl"
    checks.append(("Scalers", scaler_features.exists() and scaler_target.exists()))
    
    # Verificar dataset
    dataset_file = project_root / "data/raw/energy_consumption.csv"
    checks.append(("Dataset", dataset_file.exists()))
    
    # Exibir resultados
    all_ok = True
    for name, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
        if not status:
            all_ok = False
    
    print()
    if all_ok:
        print("🎉 Sistema saudável!")
    else:
        print("⚠️ Alguns componentes precisam de atenção")
    
    return all_ok


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Utilitários EnergyFlow AI")
    parser.add_argument("command", choices=["cleanup", "health"])
    
    args = parser.parse_args()
    
    if args.command == "cleanup":
        cleanup_logs()
    elif args.command == "health":
        check_system_health()
