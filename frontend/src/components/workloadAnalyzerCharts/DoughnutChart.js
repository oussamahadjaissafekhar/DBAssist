import React from 'react';
import { Doughnut } from 'react-chartjs-2';

function DoughnutChart({ data }) {
    const totalWhereUses = data.reduce((acc, item) => acc + item['Where Uses'], 0);
    const totalJoinUses = data.reduce((acc, item) => acc + item['Join Uses'], 0);

    const chartData = {
        labels: ['Where Uses', 'Join Uses'],
        datasets: [
            {
                data: [totalWhereUses, totalJoinUses],
                backgroundColor: ['#FF6384', '#36A2EB'],
            },
        ],
    };

    return <Doughnut data={chartData} />;
}

export default DoughnutChart;
