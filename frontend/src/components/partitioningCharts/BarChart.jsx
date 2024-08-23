import React from 'react';
import { Bar } from 'react-chartjs-2';

function BarChart({ data }) {
    const chartData = {
        labels: data.map(item => item.Attribute),
        datasets: [
            {
                label: 'Number of Updates',
                data: data.map(item => item['NumberOfUpdates']),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Frequency of updates per attribute', // Set your desired title here
                font: {
                    size: 16,
                },
                padding: {
                    bottom: 20,
                },
            },
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return `${tooltipItem.label}: ${tooltipItem.raw}`;
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Attributes',
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Number of Updates',
                },
            },
        },
    };

    return <Bar className='Bar' data={chartData} options={options} />;
}

export default BarChart;
