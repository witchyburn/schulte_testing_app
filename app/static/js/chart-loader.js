function initializePlotlyCharts() {
    const container = document.getElementById('plotly-chart');
    if (!container) return;
    
    try {
        const graph = JSON.parse(container.dataset.graph);
        Plotly.newPlot(container, graph.data, graph.layout, {
            responsive: true,
            displayModeBar: false,
            displaylogo: false
        });
    } catch (error) {
        console.error('Chart error:', error);
        container.innerHTML = '<p class="error">Ошибка загрузки графика</p>';
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePlotlyCharts);
} else {
    initializePlotlyCharts();
}