class PlotlyChartLoader {
    constructor() {
    }

    findChartContainers() {
        return document.querySelectorAll('[data-plotly-chart]');
    }

    initializeChart(container) {
        try {
            const graph = JSON.parse(container.dataset.graph);
            Plotly.newPlot(container, graph.data, graph.layout, {
                responsive: true,
                displayModeBar: false,
                displaylogo: false
            });
            
            window.addEventListener('resize', () => {
                Plotly.Plots.resize(container);
            });
            
            return true;
        } catch (error) {
            console.error('Plotly chart error:', error, container);
            container.innerHTML = `
                <div class="chart-error">
                    <p>Ошибка загрузки графика</p>
                    <small>${error.message}</small>
                </div>
            `;
            return false;
        }
    }

    initializeAllCharts() {
        const containers = this.findChartContainers();
        containers.forEach(container => {
            this.initializeChart(container);
        });
    }
}

const plotlyChartLoader = new PlotlyChartLoader();

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        plotlyChartLoader.initializeAllCharts();
    });
} else {
    plotlyChartLoader.initializeAllCharts();
}

if (typeof window !== 'undefined') {
    window.PlotlyChartLoader = PlotlyChartLoader;
}