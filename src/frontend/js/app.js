// ===================================
// ENERGYFLOW AI - JAVASCRIPT
// Sistema Inteligente de Previsão Energética
// ===================================

const API_URL = 'http://localhost:8000';

let predictionChart = null;
let isLoading = false; // Previne múltiplas chamadas simultâneas

// ===================================
// INICIALIZAÇÃO
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 EnergyFlow AI inicializado');
    
    // Verificar status da API
    checkAPIStatus();
    
    // Carregar informações do modelo (apenas uma vez)
    loadModelInfo();
    
    // Event Listeners
    setupEventListeners();
    
    // Inicializar gráfico
    initChart();
});

// ===================================
// STATUS DA API
// ===================================

async function checkAPIStatus() {
    const statusIndicator = document.getElementById('apiStatus');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusDot.classList.add('online');
            statusText.textContent = 'API Online';
            console.log('✅ API está online');
        } else {
            statusDot.classList.add('offline');
            statusText.textContent = 'Modelo não carregado';
            console.warn('⚠️ Modelo não está carregado');
        }
    } catch (error) {
        statusDot.classList.add('offline');
        statusText.textContent = 'API Offline';
        console.error('❌ Erro ao conectar com API:', error);
    }
}

// ===================================
// INFORMAÇÕES DO MODELO
// ===================================

async function loadModelInfo() {
    try {
        const response = await fetch(`${API_URL}/model/info`);
        const data = await response.json();
        
        if (data.status === 'ready') {
            document.getElementById('modelStatus').textContent = '✅ Carregado';
            document.getElementById('modelParams').textContent = data.total_params.toLocaleString();
            document.getElementById('modelFeatures').textContent = data.n_features;
            document.getElementById('modelSequence').textContent = `${data.sequence_length}h`;
        } else {
            document.getElementById('modelStatus').textContent = '❌ Não carregado';
            showError('modelStats', 'Execute o treinamento: python src/model/train.py');
        }
    } catch (error) {
        console.error('Erro ao carregar info do modelo:', error);
        document.getElementById('modelStatus').textContent = '❌ Erro';
    }
}

// ===================================
// EVENT LISTENERS
// ===================================

function setupEventListeners() {
    // Quick Prediction
    document.getElementById('btnQuickPredict').addEventListener('click', handleQuickPredict);
    
    // Manual Prediction
    document.getElementById('manualPredictForm').addEventListener('submit', handleManualPredict);
    
    // Auto-update weekend checkbox
    document.getElementById('dayOfWeek').addEventListener('change', (e) => {
        const day = parseInt(e.target.value);
        document.getElementById('isWeekend').checked = (day === 5 || day === 6);
    });
    
    // Navegação suave
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
                
                // Atualizar link ativo
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

// ===================================
// QUICK PREDICTION
// ===================================

async function handleQuickPredict() {
    // Prevenir múltiplas chamadas simultâneas
    if (isLoading) {
        console.log('⚠️ Já existe uma previsão em andamento');
        return;
    }
    
    const btn = document.getElementById('btnQuickPredict');
    const resultBox = document.getElementById('quickPredictResult');
    const hoursAhead = parseInt(document.getElementById('hoursAhead').value);
    
    // Loading state
    isLoading = true;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';
    resultBox.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/forecast`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hours_ahead: hoursAhead })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Exibir resultado
        displayQuickPrediction(data);
        
        // Atualizar gráfico
        updateChart(data.forecasts);
        
    } catch (error) {
        console.error('Erro na previsão:', error);
        showError('quickPredictResult', `Erro: ${error.message}`);
    } finally {
        isLoading = false;
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-chart-area"></i> Gerar Previsão';
    }
}

function displayQuickPrediction(data) {
    const resultBox = document.getElementById('quickPredictResult');
    
    const forecasts = data.forecasts;
    const avgConsumption = forecasts.reduce((sum, f) => sum + f.predicted_consumption, 0) / forecasts.length;
    const maxConsumption = Math.max(...forecasts.map(f => f.predicted_consumption));
    const minConsumption = Math.min(...forecasts.map(f => f.predicted_consumption));
    
    resultBox.innerHTML = `
        <div class="result-title">📊 Previsão para as próximas ${data.total_hours} horas</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">Consumo Médio</div>
                <div class="result-value">${avgConsumption.toFixed(2)} kWh</div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">Pico Máximo</div>
                <div class="result-value" style="color: var(--danger);">${maxConsumption.toFixed(2)} kWh</div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">Consumo Mínimo</div>
                <div class="result-value" style="color: var(--secondary);">${minConsumption.toFixed(2)} kWh</div>
            </div>
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: var(--light-gray); border-radius: var(--radius-md);">
            <strong>Período:</strong> ${formatDate(data.start_time)} até ${formatDate(data.end_time)}
        </div>
    `;
    
    resultBox.className = 'result-box success';
    resultBox.style.display = 'block';
}

// ===================================
// MANUAL PREDICTION
// ===================================

async function handleManualPredict(e) {
    e.preventDefault();
    
    const resultBox = document.getElementById('manualPredictResult');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Coletar dados do formulário
    const formData = {
        temperature_celsius: parseFloat(document.getElementById('temperature').value),
        hour: parseInt(document.getElementById('hour').value),
        day_of_week: parseInt(document.getElementById('dayOfWeek').value),
        month: parseInt(document.getElementById('month').value),
        is_weekend: document.getElementById('isWeekend').checked ? 1 : 0,
        is_holiday: document.getElementById('isHoliday').checked ? 1 : 0,
        consumption_lag_1h: parseFloat(document.getElementById('lag1h').value),
        consumption_lag_24h: parseFloat(document.getElementById('lag24h').value),
        consumption_lag_168h: parseFloat(document.getElementById('lag168h').value),
        consumption_rolling_mean_24h: parseFloat(document.getElementById('rollingMean').value),
        consumption_rolling_std_24h: parseFloat(document.getElementById('rollingStd').value)
    };
    
    // Loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculando...';
    resultBox.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Exibir resultado
        displayManualPrediction(data);
        
    } catch (error) {
        console.error('Erro na previsão:', error);
        showError('manualPredictResult', 'Erro ao fazer previsão. Verifique os dados e tente novamente.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-calculator"></i> Calcular Previsão';
    }
}

function displayManualPrediction(data) {
    const resultBox = document.getElementById('manualPredictResult');
    
    resultBox.innerHTML = `
        <div class="result-title">🎯 Previsão de Consumo</div>
        <div class="result-value">${data.predicted_consumption_kwh.toFixed(2)} kWh</div>
        <div style="margin-top: 1rem; font-size: 0.875rem; color: var(--gray);">
            <strong>Confiança:</strong> ${data.confidence.toUpperCase()}<br>
            <strong>Timestamp:</strong> ${formatDate(data.timestamp)}
        </div>
    `;
    
    resultBox.className = 'result-box success';
    resultBox.style.display = 'block';
}

// ===================================
// GRÁFICO
// ===================================

function initChart() {
    const ctx = document.getElementById('predictionChart');
    if (!ctx) {
        console.error('❌ Elemento canvas não encontrado');
        return;
    }
    
    predictionChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Consumo Previsto (kWh)',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 2,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(0) + ' kWh';
                        }
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        maxTicksLimit: 12
                    }
                }
            },
            animation: {
                duration: 0  // Desabilitar animações
            }
        }
    });
    
    console.log('✅ Gráfico inicializado');
}

function updateChart(forecasts) {
    if (!predictionChart) {
        console.warn('⚠️ Gráfico não está inicializado');
        return;
    }
    
    if (!forecasts || !Array.isArray(forecasts) || forecasts.length === 0) {
        console.warn('⚠️ Dados de previsão inválidos');
        return;
    }
    
    console.log(`📊 Atualizando gráfico com ${forecasts.length} pontos`);
    
    try {
        // Limitar número de pontos para evitar sobrecarga
        const maxPoints = 168; // máximo 7 dias
        const limitedForecasts = forecasts.slice(0, maxPoints);
        
        const labels = limitedForecasts.map(f => formatTime(f.timestamp));
        const data = limitedForecasts.map(f => f.predicted_consumption);
        
        // Destruir dados antigos
        predictionChart.data.labels = [];
        predictionChart.data.datasets[0].data = [];
        
        // Adicionar novos dados
        predictionChart.data.labels = labels;
        predictionChart.data.datasets[0].data = data;
        
        // Atualizar sem animação
        predictionChart.update('none');
        
        console.log('✅ Gráfico atualizado com sucesso');
    } catch (error) {
        console.error('❌ Erro ao atualizar gráfico:', error);
    }
}

// ===================================
// UTILITÁRIOS
// ===================================

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div style="color: var(--danger); font-weight: 600;">
            <i class="fas fa-exclamation-triangle"></i> ${message}
        </div>
    `;
    element.className = 'result-box error';
    element.style.display = 'block';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit'
    });
}

// ===================================
// REFRESH STATUS PERIODICAMENTE
// ===================================

// Verificar status da API a cada 60 segundos (reduzido de 30)
// Apenas verifica o status, não faz previsões automáticas
setInterval(() => {
    if (!isLoading) {
        checkAPIStatus();
    }
}, 60000);
