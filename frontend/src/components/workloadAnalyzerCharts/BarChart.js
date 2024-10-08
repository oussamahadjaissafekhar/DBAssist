import React from 'react';
import { Bar } from 'react-chartjs-2';

function BarChart({ data }) {
    const chartData = {
        labels: data.map(item => item.attribute),
        datasets: [
            {
                label: 'Where Uses',
                data: data.map(item => item['Where Uses']),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
                label: 'Join Uses',
                data: data.map(item => item['Join Uses']),
                backgroundColor: 'rgba(153, 102, 255, 0.6)',
            },
        ],
    };
    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Attribute Usage Frequency: "Where" vs "Join"',
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
                    text: 'Number of Uses',
                },
            },
        },
    };

    return <Bar className='Bar' data={chartData} options={options} />;
}

export default BarChart;
