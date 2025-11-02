"""
TESTES UNITÁRIOS - BACKEND API
Testes para validar endpoints da API.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adicionar path do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.backend.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""
    
    def test_health_check_returns_200(self):
        """Testa se health check retorna 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_has_status(self):
        """Testa se health check retorna status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "model_not_loaded"]
    
    def test_health_check_has_timestamp(self):
        """Testa se health check retorna timestamp."""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data


class TestRootEndpoint:
    """Testes para o endpoint raiz."""
    
    def test_root_returns_200(self):
        """Testa se endpoint raiz retorna 200."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_has_version(self):
        """Testa se endpoint raiz retorna versão."""
        response = client.get("/")
        data = response.json()
        assert "version" in data


class TestModelInfoEndpoint:
    """Testes para o endpoint de informações do modelo."""
    
    def test_model_info_returns_200(self):
        """Testa se model/info retorna 200."""
        response = client.get("/model/info")
        assert response.status_code == 200
    
    def test_model_info_has_status(self):
        """Testa se model/info retorna status."""
        response = client.get("/model/info")
        data = response.json()
        assert "status" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
