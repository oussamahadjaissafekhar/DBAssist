import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const generateChartData = (data) => {
  const tableAttributes = {};
  const colorMap = {};

  // Predefined colors
  const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
    '#E7E9ED', '#4D5360', '#8A89A6', '#E15759', '#76C7C0', '#59A14F'
  ];

  let colorIndex = 0;

  // Organize data by tables
  data.forEach(item => {
    if (!tableAttributes[item.Table]) {
      tableAttributes[item.Table] = [];
    }
    if (!colorMap[item.Attribute]) {
      colorMap[item.Attribute] = colors[colorIndex % colors.length];
      colorIndex++;
    }
    tableAttributes[item.Table].push({
      label: item.Attribute,
      data: item.NumberOfUpdates,
      backgroundColor: colorMap[item.Attribute],
    });
  });

  // Prepare chart data
  const labels = Object.keys(tableAttributes);
  const datasets = [];

  Object.keys(tableAttributes).forEach((table) => {
    tableAttributes[table].forEach(attr => {
      const dataset = datasets.find(ds => ds.label === attr.label);
      if (dataset) {
        dataset.data[labels.indexOf(table)] = attr.data;
      } else {
        datasets.push({
          label: attr.label,
          data: labels.map((_, i) => (tableAttributes[labels[i]].find(a => a.label === attr.label)?.data) || 0),
          backgroundColor: attr.backgroundColor,
        });
      }
    });
  });

  return {
    labels,
    datasets
  };
};

const StackedBarChart = ({ data }) => {
  const chartData = generateChartData(data);

  return (
      <Bar className='Bar'
        data={chartData}
        options={{
          plugins: {
            title: {
                display: true,
                text: 'Stacked Bar chart of Update Frequencies by table and attribute', // Set your desired title here
                font: {
                    size: 16,
                },
                padding: {
                    bottom: 20,
                },
            },
            legend: {
                display: false,
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
        }}
      />
  );
};

export default StackedBarChart;
