document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/estadisticas')
        .then(response => {
          if (!response.ok) {
            throw new Error("Hubo un problema al intentar establecer una conexión")
          }
          return response.json() // parseamos
        })
        .then(data => {
            // gráfico de líneas
            const lineLabels = data.actividades_por_dia.map(e => e.fecha);
            const lineData = data.actividades_por_dia.map(e => e.cantidad);
            new Chart(document.getElementById('graficoLineas').getContext('2d'), {
                type: 'line',
                data: {
                    labels: lineLabels,
                    datasets: [{
                        label: 'Actividades por día',
                        data: lineData,
                        borderColor: 'blue',
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // gráfico de torta
            const pieLabels = data.actividades_por_tema.map(e => e.tema);
            const pieData = data.actividades_por_tema.map(e => e.cantidad);
            new Chart(document.getElementById('graficoTorta').getContext('2d'), {
                type: 'pie',
                data: {
                    labels: pieLabels,
                    datasets: [{
                        data: pieData,
                        backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71', '#e74c3c', '#f1c40f']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // gráfico de barras
            const barLabels = Object.keys(data.actividades_por_franja_mes);
            const franjas = ['mañana', 'mediodía', 'tarde'];
            const barDatasets = franjas.map((franja, idx) => ({
                label: franja.charAt(0).toUpperCase() + franja.slice(1),
                data: barLabels.map(mes => data.actividades_por_franja_mes[mes][franja]),
                backgroundColor: ['#3498db', '#e67e22', '#9b59b6'][idx]
            }));

            new Chart(document.getElementById('graficoBarras').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: barLabels,
                    datasets: barDatasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Error al cargar estadísticas:', err));
});