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

    return <Bar className='Bar' data={chartData} />;
}

export default BarChart;
