
import axios from 'axios'
import ReactFlow, {
    ReactFlowProvider,
    Handle,
    Node,
    Position,
    Edge,
  } from 'react-flow-renderer';

interface CustomNodeData {
    label: string;
  }
  

const CustomNodeComponent: React.FC<{ data: CustomNodeData }> = ({ data }) => {
    const nodeStyle: React.CSSProperties = {
      border: '1px solid #000',
      padding: 10,
      borderRadius: 5,
      minWidth: 150,
      textAlign: 'center',
      backgroundColor: 'white',
      display:'flex',
      justifyContent:'center'
    };
  
    return (
      <div style={nodeStyle}>
        <Handle type="target" position={Position.Top} style={{ background: '#555' }} />
        {data.label}
        <Handle type="source" position={Position.Bottom} style={{ background: '#555' }} />
      </div>
    );
  };
const nodeTypes = {
  customNode: CustomNodeComponent,
};

const nodes: Node<CustomNodeData>[] = [
  { id: '0', type: 'customNode', data: { label: 'Для консультации напишите /консультация' }, position: { x: 450, y: 0 } },
  { id: '1', type: 'customNode', data: { label: '/консультация' }, position: { x: 550, y: 125 } },
  { id: '2', type: 'customNode', data: { label: 'Здравствуйте. Ваша заявка на консультацию принята. Как вам удобно переговорить устно ( /позвоните_мне) или перепиской ( /напишите_мне)?' }, position: { x: 43, y: 225 } },
  { id: '3a', type: 'customNode', data: { label: '/позвоните_мне' }, position: { x: 300, y: 325 } },
  { id: '3b', type: 'customNode', data: { label: '/напишите_мне' }, position: { x: 900, y: 325 } },
  { id: '4', type: 'customNode', data: { label: ' Ок. Первый освободившийся менеджер с вами свяжется. Спасибо за обращение.' }, position: { x: 340, y: 425 } }
];

const edges: Edge[] = [
    { id: 'e0-1', source: '0', target: '1', animated: true, style: { stroke: '#000' } },
    { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#000' } },
    { id: 'e2-3a', source: '2', target: '3a', animated: true, style: { stroke: '#000' } },
    { id: 'e2-3b', source: '2', target: '3b', animated: true, style: { stroke: '#000' } },
    { id: 'e3a-4', source: '3a', target: '4', animated: true, style: { stroke: '#000' } },
    { id: 'e3b-4', source: '3b', target: '4', animated: true, style: { stroke: '#000' } }
  ];

// const [phone, setPhone] = useState<string | number | undefined>('+7XXXXXXXXXX');

const ChatbotFlow: React.FC = () => {

    const exportToJson = async () => {
        const dataToExport = {
          nodes: nodes.map(node => ({ id: node.id, label: node.data.label })),
        };
      
        const json = JSON.stringify(dataToExport, null, 1);
        console.log(json); 

        try {
            const response = await axios.post('http://127.0.0.1:5000/save-flow', dataToExport);
            console.log(response.data.message); // 'Flow saved successfully'
           
          } catch (error) {
            console.error('Error saving flow:', error);
          
          }
      };

    return (
      <ReactFlowProvider>
        <div style={{ width: '1000px', height: '1000px', background: 'lightgrey', paddingTop: '0', borderRadius: '5px' }}>
        <div style={{border:'1px solid black', padding: '30px' }}>
                <button style={{}} onClick={exportToJson}>Экспорт в JSON</button>
                {/* <input type='text' 
                        placeholder='phoneNumber' 
                        value={phone} 
                        onChange={(e)=>setPhone(e.target.value)}/> */}
            </div>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            nodesConnectable={false}
            nodesDraggable={false}
            fitView
          >   
          
          </ReactFlow>
        </div>
        
      </ReactFlowProvider>
    );
  };

export default ChatbotFlow;