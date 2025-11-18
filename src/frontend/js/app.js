// ===================================
// ENERGYFLOW AI - JAVASCRIPT
// Sistema Inteligente de Previsão Energética
// Versão 3.0 - Inteligência Artificial Avançada
// ===================================

// Detectar automaticamente a URL da API (desenvolvimento vs produção)
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://energyflow-api.onrender.com';

const MODEL_ACCURACY = '99.97%';

let predictionChart = null;
let isLoading = false;
let apiStatusInterval = null;
let scrollTopBtn = null;
let scrollProgressBar = null;

// ===================================
// INICIALIZAÇÃO
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('%c🚀 EnergyFlow AI v3.0 inicializado', 'color: #667eea; font-size: 16px; font-weight: bold;');
    
    // Verificar status da API
    checkAPIStatus();
    
    // Carregar informações do modelo
    loadModelInfo();
    
    // Event Listeners
    setupEventListeners();
    
    // Inicializar gráfico
    initChart();
    
    // Animações de entrada
    animateOnScroll();
    
    // Verificar status periodicamente
    startAPIStatusMonitoring();
    
    // Adicionar tooltips dinâmicos
    initializeTooltips();
    
    initHeroBadges();
    initScrollUtilities();
    
    console.log('%c✅ Sistema pronto para uso!', 'color: #10b981; font-weight: bold;');
});

// ===================================
// STATUS DA API - APRIMORADO
// ===================================

async function checkAPIStatus() {
    const statusIndicator = document.getElementById('apiStatus');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    try {
        const startTime = performance.now();
        const response = await fetch(`${API_URL}/health`);
        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusDot.classList.remove('offline');
            statusDot.classList.add('online');
            statusText.innerHTML = `🟢 API Online <small style="opacity: 0.8;">(${responseTime}ms)</small>`;
            statusText.style.color = '#10b981';
            console.log(`%c✅ API respondeu em ${responseTime}ms`, 'color: #10b981;');
            updateLatencyBadge(`${responseTime} ms`);
            updateDeployBadge('Online', true);
            
            // Notificação visual sutil
            showToast('✅ Conectado à API com sucesso!', 'success', 2000);
        } else {
            statusDot.classList.remove('online');
            statusDot.classList.add('offline');
            statusText.textContent = '⚠️ Modelo não carregado';
            statusText.style.color = '#f59e0b';
            console.warn('⚠️ Modelo não está carregado');
            updateDeployBadge('Modelo indisponível', false);
        }
    } catch (error) {
        statusDot.classList.remove('online');
        statusDot.classList.add('offline');
        statusText.innerHTML = '🔴 API Offline';
        statusText.style.color = '#ef4444';
        console.error('%c❌ Erro ao conectar com API:', 'color: #ef4444; font-weight: bold;', error);
        showToast('❌ Não foi possível conectar à API', 'error', 3000);
        updateDeployBadge('Offline', false);
        updateLatencyBadge('--');
    }
}

function startAPIStatusMonitoring() {
    // Verificar a cada 60 segundos
    apiStatusInterval = setInterval(() => {
        if (!isLoading) {
            checkAPIStatus();
        }
    }, 60000);
}

// Toast notification system
function showToast(message, type = 'info', duration = 3000) {
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) existingToast.remove();
    
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 1.25rem;">${getToastIcon(type)}</span>
            <span>${message}</span>
        </div>
    `;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
        border-left: 4px solid ${getToastColor(type)};
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function getToastIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

function getToastColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    return colors[type] || colors.info;
}

// ===================================
// INFORMAÇÕES DO MODELO - APRIMORADO
// ===================================

async function loadModelInfo() {
    const modelStatus = document.getElementById('modelStatus');
    const modelParams = document.getElementById('modelParams');
    const modelFeatures = document.getElementById('modelFeatures');
    const modelSequence = document.getElementById('modelSequence');
    
    try {
        const response = await fetch(`${API_URL}/health`);
        
        // Verificar se a resposta é OK
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.model_loaded && data.model_info) {
            const modelInfo = data.model_info;
            
            // Atualizar informações do modelo
            if (modelInfo.n_estimators) {
                modelParams.textContent = modelInfo.n_estimators.toLocaleString();
            } else if (modelInfo.n_base_models) {
                modelParams.textContent = `${modelInfo.n_base_models} modelos`;
            } else {
                modelParams.textContent = 'Ensemble';
            }
            
            if (modelInfo.n_features) {
                modelFeatures.textContent = modelInfo.n_features.toLocaleString();
            } else {
                modelFeatures.textContent = '-';
            }
            
            modelStatus.innerHTML = '<span class="badge badge-success">✅ Carregado</span>';
            modelSequence.innerHTML = '<strong>Regressão ML</strong>';
            
            // Log das informações do modelo
            console.log('%cℹ️ Informações do Modelo:', 'color: #3b82f6; font-weight: bold;');
            if (modelInfo.n_estimators) {
                console.log('  🌳 Estimadores:', modelInfo.n_estimators.toLocaleString());
            }
            if (modelInfo.n_base_models) {
                console.log('  🔀 Modelos base:', modelInfo.n_base_models);
            }
            console.log('  🔢 Features:', modelInfo.n_features || '-');
            console.log('  📐 Tipo:', modelInfo.model_type || 'Ensemble');
            
        } else {
            // Modelo não está pronto
            modelStatus.innerHTML = '<span class="badge badge-warning">❌ Não carregado</span>';
            modelParams.textContent = '-';
            modelFeatures.textContent = '-';
            modelSequence.innerHTML = '<strong>Não disponível</strong>';
            
            const message = data.message || '⚠️ Modelo não está pronto. Execute o treinamento com: <code>python src/model/train.py</code>';
            showError('modelStats', message);
            
            console.warn('⚠️ Modelo não está pronto:', data);
        }
    } catch (error) {
        console.error('Erro ao carregar info do modelo:', error);
        modelStatus.innerHTML = '<span class="badge badge-warning">❌ Erro</span>';
        modelParams.textContent = '-';
        modelFeatures.textContent = '-';
        modelSequence.innerHTML = '<strong>Erro ao carregar</strong>';
        
        // Mostrar mensagem de erro mais amigável
        showError('modelStats', 
            `⚠️ Erro ao conectar com a API. Verifique se o servidor está rodando em ${API_URL}<br>` +
            `💡 Sugestões:<br>` +
            `• Verifique se a API está rodando (deve mostrar "API Online" no topo)<br>` +
            `• Tente novamente em alguns segundos<br>` +
            `• Se o erro persistir, verifique o console do navegador (F12).`);
    }
}

// Animação de contagem progressiva
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString('pt-BR');
    }, 16);
}

// ===================================
// EVENT LISTENERS - EXPANDIDO
// ===================================

function setupEventListeners() {
    // Quick Prediction
    document.getElementById('btnQuickPredict').addEventListener('click', handleQuickPredict);
    
    // Manual Prediction
    document.getElementById('manualPredictForm').addEventListener('submit', handleManualPredict);
    
    // Auto-update weekend checkbox
    document.getElementById('dayOfWeek').addEventListener('change', (e) => {
        const day = parseInt(e.target.value);
        const weekendCheckbox = document.getElementById('isWeekend');
        weekendCheckbox.checked = (day === 5 || day === 6);
        
        // Feedback visual
        if (weekendCheckbox.checked) {
            weekendCheckbox.parentElement.style.animation = 'pulse 0.3s ease';
        }
    });
    
    // Validação em tempo real dos inputs numéricos
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            validateInput(e.target);
        });
        
        // Adicionar efeito de foco
        input.addEventListener('focus', (e) => {
            e.target.parentElement.style.transform = 'scale(1.02)';
            e.target.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        input.addEventListener('blur', (e) => {
            e.target.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // Navegação suave com indicador ativo
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            
            if (target) {
                // Scroll suave
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Atualizar link ativo
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Efeito de destaque na seção
                target.style.animation = 'none';
                setTimeout(() => {
                    target.style.animation = 'highlightSection 0.6s ease';
                }, 10);
            }
        });
    });
    
    // Slider de horas com preview em tempo real
    const hoursSlider = document.getElementById('hoursAhead');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', (e) => {
            updateHoursPreview(e.target.value);
        });
    }
}

function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    if (value < min || value > max) {
        input.style.borderColor = '#ef4444';
        input.style.animation = 'shake 0.3s ease';
    } else {
        input.style.borderColor = '#10b981';
        setTimeout(() => {
            input.style.borderColor = '';
        }, 1000);
    }
}

function updateHoursPreview(hours) {
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;
    let preview = `${hours}h`;
    
    if (days > 0) {
        preview = `${days} dia${days > 1 ? 's' : ''}`;
        if (remainingHours > 0) {
            preview += ` e ${remainingHours}h`;
        }
    }
    
    // Criar ou atualizar preview
    let previewElement = document.getElementById('hoursPreview');
    if (!previewElement) {
        previewElement = document.createElement('small');
        previewElement.id = 'hoursPreview';
        previewElement.style.cssText = 'color: var(--gray); display: block; margin-top: 0.25rem; font-weight: 500;';
        document.getElementById('hoursAhead').parentElement.appendChild(previewElement);
    }
    previewElement.textContent = `📅 Equivale a: ${preview}`;
}

// ===================================
// QUICK PREDICTION - ULTRA APRIMORADO
// ===================================

async function handleQuickPredict() {
    // Prevenir múltiplas chamadas
    if (isLoading) {
        showToast('⏳ Aguarde a previsão anterior finalizar', 'warning', 2000);
        return;
    }
    
    const btn = document.getElementById('btnQuickPredict');
    const resultBox = document.getElementById('quickPredictResult');
    const hoursAhead = parseInt(document.getElementById('hoursAhead').value);
    
    // Validação
    if (hoursAhead < 1 || hoursAhead > 168) {
        showToast('❌ Escolha entre 1 e 168 horas (7 dias)', 'error', 3000);
        return;
    }
    
    // Loading state com animação
    isLoading = true;
    btn.disabled = true;
    btn.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div class="spinner" style="width: 20px; height: 20px;"></div>
            <span>Analisando padrões...</span>
        </div>
    `;
    resultBox.style.display = 'none';
    
    // Progress bar simulada
    showProgressBar();
    
    try {
        console.log(`%c🔮 Gerando previsão para ${hoursAhead} horas...`, 'color: #667eea; font-weight: bold;');
        
        const startTime = performance.now();
        const response = await fetch(`${API_URL}/forecast`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hours_ahead: hoursAhead })
        });
        
        const endTime = performance.now();
        const processingTime = Math.round(endTime - startTime);
        
        if (!response.ok) {
            let errorMessage = `Erro HTTP ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                // Se não conseguir parsear JSON, usar mensagem padrão
                if (response.status === 404) {
                    errorMessage = `Endpoint não encontrado. Verifique se o servidor está rodando e se os endpoints estão registrados.`;
                }
            }
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        
        console.log(`%c✅ Previsão concluída em ${processingTime}ms`, 'color: #10b981; font-weight: bold;');
        console.log('📊 Dados recebidos:', data);
        
        // Exibir resultado com animação
        setTimeout(() => {
            displayQuickPrediction(data, processingTime);
            updateChart(data.forecasts);
            showToast(`✅ ${hoursAhead} horas previstas com sucesso!`, 'success', 3000);
        }, 500);
        
    } catch (error) {
        console.error('%c❌ Erro na previsão:', 'color: #ef4444; font-weight: bold;', error);
        showError('quickPredictResult', `
            <strong>Erro ao gerar previsão:</strong><br>
            ${error.message}
        `);
        showToast('❌ Erro ao gerar previsão', 'error', 4000);
    } finally {
        isLoading = false;
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-chart-area"></i> Gerar Previsão Automática';
        hideProgressBar();
    }
}

function showProgressBar() {
    const progressContainer = document.createElement('div');
    progressContainer.id = 'progressContainer';
    progressContainer.innerHTML = `
        <div class="progress-bar" style="margin-top: 1rem;">
            <div class="progress-fill" id="progressFill" style="width: 0%;"></div>
        </div>
        <p class="loading-text" style="margin-top: 0.5rem;">Processando dados históricos...</p>
    `;
    
    const resultBox = document.getElementById('quickPredictResult');
    resultBox.parentElement.insertBefore(progressContainer, resultBox);
    
    // Animar progress bar
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        document.getElementById('progressFill').style.width = progress + '%';
    }, 200);
    
    progressContainer.dataset.intervalId = progressInterval;
}

function hideProgressBar() {
    const progressContainer = document.getElementById('progressContainer');
    if (progressContainer) {
        clearInterval(progressContainer.dataset.intervalId);
        const progressFill = document.getElementById('progressFill');
        if (progressFill) progressFill.style.width = '100%';
        
        setTimeout(() => {
            progressContainer.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => progressContainer.remove(), 300);
        }, 300);
    }
}

function displayQuickPrediction(data) {
    const resultBox = document.getElementById('quickPredictResult');
    
    // Validar dados
    if (!data || !data.forecasts || !Array.isArray(data.forecasts) || data.forecasts.length === 0) {
        showError('quickPredictResult', 'Erro: Dados de previsão inválidos ou vazios.');
        return;
    }
    
    const forecasts = data.forecasts;
    const avgConsumption = forecasts.reduce((sum, f) => sum + (f.predicted_consumption || 0), 0) / forecasts.length;
    const maxConsumption = Math.max(...forecasts.map(f => f.predicted_consumption || 0));
    const minConsumption = Math.min(...forecasts.map(f => f.predicted_consumption || 0));
    
    // Validar valores
    if (isNaN(avgConsumption) || isNaN(maxConsumption) || isNaN(minConsumption)) {
        showError('quickPredictResult', 'Erro: Valores de previsão inválidos.');
        return;
    }
    
    resultBox.innerHTML = `
        <div class="result-title">📊 Previsão Concluída!</div>
        <p style="color: var(--gray); margin-bottom: 1rem;">
            Analisamos os dados históricos e previmos o consumo de energia para as próximas <strong>${data.total_hours} horas</strong> 
            (${Math.round(data.total_hours / 24 * 10) / 10} dias). Aqui está um resumo do que esperamos:
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">
                    📊 Consumo Médio Esperado
                    <br><small style="font-size: 0.75rem;">(quanto de energia você vai gastar em média a cada hora durante todo o período previsto)</small>
                </div>
                <div class="result-value">${avgConsumption.toFixed(2)} kWh</div>
                <div style="font-size: 0.75rem; color: var(--gray); margin-top: 0.25rem;">
                    ≈ ${(avgConsumption * 24).toFixed(2)} kWh por dia
                </div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">
                    ⚠️ Pico Máximo de Consumo
                    <br><small style="font-size: 0.75rem;">(o maior consumo previsto em uma única hora - geralmente quando mais aparelhos estão ligados)</small>
                </div>
                <div class="result-value" style="color: var(--danger);">${maxConsumption.toFixed(2)} kWh</div>
                <div style="font-size: 0.75rem; color: var(--gray); margin-top: 0.25rem;">
                    ${maxConsumption > avgConsumption * 1.5 ? '⚠️ Muito acima da média' : 'Dentro do esperado'}
                </div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: var(--gray);">
                    ✅ Consumo Mínimo
                    <br><small style="font-size: 0.75rem;">(o menor consumo previsto em uma única hora - geralmente quando poucos aparelhos estão ligados)</small>
                </div>
                <div class="result-value" style="color: var(--secondary);">${minConsumption.toFixed(2)} kWh</div>
                <div style="font-size: 0.75rem; color: var(--gray); margin-top: 0.25rem;">
                    ${avgConsumption > 0 ? `Economia de ${((avgConsumption - minConsumption) / avgConsumption * 100).toFixed(1)}% vs média` : 'Valor mínimo'}
                </div>
            </div>
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: var(--light-gray); border-radius: var(--radius-md);">
            <strong>⏰ Período da Previsão:</strong><br>
            De ${formatDate(data.start_time)} até ${formatDate(data.end_time)}
            <br><small style="color: var(--gray); font-size: 0.875rem;">
                (Previsão de ${data.total_hours} horas consecutivas)
            </small>
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: #e8f4f8; border-radius: var(--radius-md); border-left: 4px solid #667eea;">
            💡 <strong>Como interpretar:</strong> O gráfico abaixo mostra como o consumo de energia varia hora por hora. 
            Linhas mais altas = mais consumo. Use isso para planejar quando ligar aparelhos que consomem muita energia!
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-radius: var(--radius-md); border-left: 4px solid #ffc107;">
            📊 <strong>Consumo Total Estimado:</strong> ${(avgConsumption * data.total_hours).toFixed(2)} kWh 
            (média × ${data.total_hours} horas). 
            <br><small style="color: var(--gray);">
                💰 Se cada kWh custa R$ 0,80, isso representa aproximadamente R$ ${(avgConsumption * data.total_hours * 0.80).toFixed(2)} no período.
            </small>
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
    
    // Interpretação do resultado
    let interpretation = '';
    const consumption = data.predicted_consumption_kwh;
    
    if (consumption < 0.5) {
        interpretation = 'Consumo <strong>muito baixo</strong> - poucos aparelhos ligados (lâmpadas, TV, carregadores). Equivale a uma casa quase vazia.';
    } else if (consumption < 1.0) {
        interpretation = 'Consumo <strong>baixo</strong> - uso normal de aparelhos básicos (geladeira, TV, computador, lâmpadas). É o consumo típico de uma casa com poucas pessoas.';
    } else if (consumption < 2.0) {
        interpretation = 'Consumo <strong>moderado</strong> - vários aparelhos em uso ao mesmo tempo (geladeira, TV, computador, máquina de lavar, etc.). É o consumo normal de uma família pequena.';
    } else if (consumption < 3.0) {
        interpretation = 'Consumo <strong>alto</strong> - muitos aparelhos ligados simultaneamente ou uso de equipamentos potentes (micro-ondas, secadora, vários computadores). Família grande ou uso intensivo.';
    } else {
        interpretation = 'Consumo <strong>muito alto</strong> - uso intensivo de energia (ar-condicionado, aquecedor elétrico, chuveiro elétrico, ou muitos aparelhos potentes ligados ao mesmo tempo).';
    }
    
    resultBox.innerHTML = `
        <div class="result-title">🎯 Resultado da Previsão Personalizada</div>
        <div class="result-value">${data.predicted_consumption_kwh.toFixed(2)} kWh</div>
        <div style="margin-top: 1rem; padding: 1rem; background: #f0f7ff; border-radius: var(--radius-md); border-left: 4px solid #667eea;">
            <strong>📖 O que isso significa?</strong><br>
            ${interpretation}
        </div>
        <div style="margin-top: 1rem; font-size: 0.875rem; color: var(--gray);">
            <strong>ℹ️ Detalhes técnicos:</strong><br>
            • Confiança da IA: <strong>${data.confidence.toUpperCase()}</strong> (alta = mais precisa)<br>
            • Calculado em: ${formatDate(data.timestamp)}<br>
            • kWh = quilowatt-hora (unidade da conta de luz)
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-radius: var(--radius-md); border-left: 4px solid #ffc107;">
            💡 <strong>Referência para entender o valor:</strong> 
            <br>• Uma casa pequena (1-2 pessoas): 0.5 a 1.5 kWh por hora
            <br>• Uma casa média (3-4 pessoas): 1.0 a 2.5 kWh por hora  
            <br>• Uma casa grande (5+ pessoas): 1.5 a 3.5 kWh por hora
            <br><br>
            <strong>Exemplos práticos:</strong>
            <br>• 1 kWh = deixar 10 lâmpadas LED (10W cada) ligadas por 10 horas
            <br>• 1 kWh = usar um ar-condicionado de 12.000 BTUs por 1 hora
            <br>• 1 kWh = tomar um banho de 15 minutos no chuveiro elétrico (4.500W)
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
                            return value.toFixed(2) + ' kWh';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Consumo de Energia (kWh)'
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
            <i class="fas fa-exclamation-triangle"></i> <strong>Ops! Algo deu errado</strong>
        </div>
        <div style="margin-top: 0.5rem; color: var(--gray);">
            ${message}
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-radius: var(--radius-md);">
            💡 <strong>Sugestões:</strong><br>
            • Verifique se a API está rodando (deve mostrar "API Online" no topo)<br>
            • Tente novamente em alguns segundos<br>
            • Se o erro persistir, verifique o console do navegador (F12)
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
// ANIMAÇÕES E EFEITOS VISUAIS
// ===================================

function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-out';
                entry.target.style.opacity = '1';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.card, .stat-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

function initializeTooltips() {
    // Adicionar tooltips informativos
    const tooltips = {
        'temperature': 'A temperatura influencia muito o consumo de energia (ar-condicionado, aquecimento)',
        'hour': 'Diferentes horários têm padrões diferentes (pico pela manhã e noite)',
        'dayOfWeek': 'Dias úteis geralmente têm consumo diferente dos finais de semana',
        'month': 'O mês do ano afeta sazonalmente o consumo (verão vs inverno)',
        'lag1h': 'Consumo de 1 hora atrás - ajuda a IA entender a tendência recente',
        'lag24h': 'Consumo de ontem no mesmo horário - padrão diário',
        'lag168h': 'Consumo da semana passada - padrão semanal',
        'rollingMean': 'Média móvel das últimas 24h - suaviza variações',
        'rollingStd': 'Desvio padrão - indica variabilidade do consumo'
    };
    
    Object.keys(tooltips).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.setAttribute('title', tooltips[id]);
            element.style.cursor = 'help';
        }
    });
}

function initHeroBadges() {
    updateHeroAccuracy();
    updateLatencyBadge('--');
    updateDeployBadge('Verificando...', true);
}

function updateHeroAccuracy() {
    setBadgeValue('badgeAccuracy', MODEL_ACCURACY);
}

function updateLatencyBadge(value) {
    setBadgeValue('badgeLatency', value);
}

function updateDeployBadge(text, isOnline = true) {
    const badge = document.getElementById('badgeDeploy');
    if (badge) {
        badge.textContent = text;
        badge.classList.toggle('badge-offline', !isOnline);
    }
}

function setBadgeValue(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

function initScrollUtilities() {
    scrollTopBtn = document.getElementById('scrollTopButton');
    scrollProgressBar = document.getElementById('scrollProgressBar');
    
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    window.addEventListener('scroll', handleScrollUtilities, { passive: true });
    handleScrollUtilities();
}

function handleScrollUtilities() {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = docHeight > 0 ? (scrollPosition / docHeight) * 100 : 0;
    
    if (scrollProgressBar) {
        scrollProgressBar.style.width = `${progress}%`;
    }
    
    if (scrollTopBtn) {
        if (scrollPosition > 400) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    }
}

// ===================================
// ESTATÍSTICAS EM TEMPO REAL
// ===================================

function displayAdvancedStats(forecasts) {
    const stats = calculateAdvancedStats(forecasts);
    
    console.group('📊 Estatísticas Detalhadas');
    console.log('📈 Tendência:', stats.trend);
    console.log('📊 Variância:', stats.variance.toFixed(2));
    console.log('⚡ Consumo Total Previsto:', stats.totalConsumption.toFixed(2) + ' kWh');
    console.log('💰 Estimativa de Custo (R$ 0.80/kWh):', 'R$ ' + (stats.totalConsumption * 0.80).toFixed(2));
    console.log('🌱 Emissões CO2 estimadas:', (stats.totalConsumption * 0.5).toFixed(2) + ' kg');
    console.groupEnd();
    
    return stats;
}

function calculateAdvancedStats(forecasts) {
    const values = forecasts.map(f => f.predicted_consumption);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
    
    // Calcular tendência
    let trend = 'estável';
    const first = values.slice(0, values.length / 3).reduce((a, b) => a + b, 0) / (values.length / 3);
    const last = values.slice(-values.length / 3).reduce((a, b) => a + b, 0) / (values.length / 3);
    
    if (last > first * 1.1) trend = 'crescente ↗️';
    else if (last < first * 0.9) trend = 'decrescente ↘️';
    else trend = 'estável ➡️';
    
    return {
        mean,
        variance,
        trend,
        totalConsumption: values.reduce((a, b) => a + b, 0)
    };
}

// ===================================
// EXPORT FUNCTIONS
// ===================================

function exportPredictionData(data) {
    const csv = convertToCSV(data.forecasts);
    downloadFile(csv, 'previsao_energetica.csv', 'text/csv');
    showToast('📥 Dados exportados com sucesso!', 'success', 2000);
}

function convertToCSV(forecasts) {
    const headers = ['Timestamp', 'Consumo Previsto (kWh)'];
    const rows = forecasts.map(f => [f.timestamp, f.predicted_consumption.toFixed(3)]);
    
    return [
        headers.join(','),
        ...rows.map(r => r.join(','))
    ].join('\n');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

// ===================================
// PERFORMANCE MONITORING
// ===================================

function logPerformance(operation, duration) {
    const performance = {
        operation,
        duration: `${duration}ms`,
        timestamp: new Date().toISOString()
    };
    
    console.log(`%c⚡ Performance: ${operation} completado em ${duration}ms`, 
                'color: #f59e0b; font-weight: bold;');
    
    return performance;
}

// ===================================
// KEYBOARD SHORTCUTS
// ===================================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter para executar previsão rápida
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        const quickPredictBtn = document.getElementById('btnQuickPredict');
        if (quickPredictBtn && !quickPredictBtn.disabled) {
            quickPredictBtn.click();
            showToast('⌨️ Atalho: Ctrl+Enter', 'info', 1500);
        }
    }
    
    // Escape para limpar resultados
    if (e.key === 'Escape') {
        const resultBoxes = document.querySelectorAll('.result-box');
        resultBoxes.forEach(box => {
            box.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => box.style.display = 'none', 300);
        });
    }
});

// ===================================
// ADICIONAR CSS DINÂMICO
// ===================================

const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes highlightSection {
        0% { background: transparent; }
        50% { background: rgba(102, 126, 234, 0.05); }
        100% { background: transparent; }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    .spinner {
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-top: 3px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
`;
document.head.appendChild(style);

// ===================================
// INICIALIZAÇÃO FINAL
// ===================================

console.log('%c' + `
╔═══════════════════════════════════════════════════╗
║   🚀 EnergyFlow AI v3.0                          ║
║   Sistema Inteligente de Previsão Energética    ║
║   Powered by Advanced AI (Ensemble ML)           ║
║   Desenvolvido com ❤️ • Novembro 2025           ║
╚═══════════════════════════════════════════════════╝
`, 'color: #667eea; font-weight: bold; font-family: monospace; font-size: 12px;');

console.log('%c� Sistema Iniciado com Sucesso!', 'color: #10b981; font-weight: bold; font-size: 14px;');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #667eea;');

console.log('%c📋 Atalhos de Teclado:', 'color: #3b82f6; font-weight: bold;');
console.log('  • %cCtrl+Enter%c → Executar previsão rápida', 'color: #f59e0b; font-weight: bold;', 'color: inherit;');
console.log('  • %cEsc%c → Limpar resultados', 'color: #f59e0b; font-weight: bold;', 'color: inherit;');
console.log('  • %cF12%c → Abrir DevTools', 'color: #f59e0b; font-weight: bold;', 'color: inherit;');
console.log('');

console.log('%c🛠️ Tecnologias:', 'color: #8b5cf6; font-weight: bold;');
console.log('  • Frontend: HTML5, CSS3, Vanilla JS');
console.log('  • Backend: FastAPI + Python 3.11');
console.log('  • IA: Scikit-learn + XGBoost (Regressão ML)');
console.log('  • Data: 2.049.280 medições reais');
console.log('');

console.log('%c💡 Dica Pro:', 'color: #10b981; font-weight: bold;');
console.log('  Todos os logs detalhados aparecem aqui no console!');
console.log('  Use as ferramentas de desenvolvedor para debug.');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #667eea;');

// ===================================
// ENHANCED STAT CARD ANIMATIONS
// ===================================

document.querySelectorAll('.stat-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.zIndex = '10';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.zIndex = '1';
    });
});

// ===================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ===================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            // Highlight section briefly
            target.style.animation = 'highlightSection 2s ease';
            setTimeout(() => {
                target.style.animation = '';
            }, 2000);
        }
    });
});

// ===================================
// PARTICLE EFFECT ON HERO (Optional)
// ===================================

function createParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 3 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = 'rgba(255,255,255,0.3)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${Math.random() * 10 + 10}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';
        hero.appendChild(particle);
    }
}

// Uncomment to enable particles:
// createParticles();
