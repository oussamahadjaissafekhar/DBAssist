import React from 'react';
import ReactFlow, { Background } from 'react-flow-renderer';

function ERDiagram({ nodes, edges }) {
  return (
    <div style={{ height: '200%', width: '200%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ height: '100%', width: '90%' }}>
        <ReactFlow nodes={nodes} edges={edges}>
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
}

export default ERDiagram;

