import React from 'react';
import { Pie } from 'react-chartjs-2';

function PieChart({ data }) {
    const chartData = {
        labels: data.map(item => item.Attribute),
        datasets: [
            {
                label: 'Number of Updates',
                data: data.map(item => item['NumberOfUpdates']),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                ],
                borderWidth: 1,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false, // Disable to allow custom height/width
        plugins: {
            title: {
                display: true,
                text: 'Distribution of Updates per Attribute',
                font: {
                    size: 16,
                },
                padding: {
                    bottom: 20,
                },
            },
            legend: {
                display: true,
                position: 'right', // Change to 'bottom' or 'left' as needed
                labels: {
                    font: {
                        size: 12, // Reduce legend font size
                    },
                },
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        const label = tooltipItem.label || '';
                        const value = tooltipItem.raw || '';
                        return `${label}: ${value}`;
                    }
                }
            }
        },
    };

    const chartStyle = {
        width: '500px', 
        height: '500px',
        margin: 'auto',
    };

    return <div style={chartStyle}><Pie className='Pie' data={chartData} options={options} /></div>;
}

export default PieChart;
