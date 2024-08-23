import React from 'react';
import { Bar } from 'react-chartjs-2';

function StackedBarChart({ data }) {
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
        plugins: {
            title: {
                display: true,
                text: 'Stacked Bar Chart of Access Frequency by Attribute for "Join" and "Where" Uses',
                font: {
                    size: 16,
                },
                padding: {
                    bottom: 20,
                },
            },
            legend: {
                display: false, // Hide the legend
              },
            tooltip: {
              callbacks: {
                label: (context) => `${context.dataset.label}: ${context.raw}`
              }
            }
          },
          responsive: true,
          scales: {
            x: {
              stacked: true,
              title: {
                display: true,
                text: 'Attributes',
            },
            },
            y: {
              stacked: true,
              title: {
                display: true,
                text: 'Number of Updates',
            },
            }
          }
    };

    return <Bar className='Bar' data={chartData} options={options} />;
}

export default StackedBarChart;
