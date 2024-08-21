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
        scales: {
            x: { stacked: true },
            y: { stacked: true },
        },
    };

    return <Bar className='Bar' data={chartData} options={options} />;
}

export default StackedBarChart;
