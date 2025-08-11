const gridEl = document.getElementById('grid');
const msgEl  = document.getElementById('msg');

const PUZZLES = {
  easy: [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9],
  ],
  medium: [
    [0,0,0,2,6,0,7,0,1],
    [6,8,0,0,7,0,0,9,0],
    [1,9,0,0,0,4,5,0,0],
    [8,2,0,1,0,0,0,4,0],
    [0,0,4,6,0,2,9,0,0],
    [0,5,0,0,0,3,0,2,8],
    [0,0,9,3,0,0,0,7,4],
    [0,4,0,0,5,0,0,3,6],
    [7,0,3,0,1,8,0,0,0],
  ],
  hard: [
    [0,0,0,0,0,0,0,1,2],
    [0,0,0,0,0,0,0,0,0],
    [0,0,1,0,9,4,0,0,0],
    [0,0,0,0,0,0,3,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,8,0,0,0,0,0,0],
    [0,0,0,7,0,0,2,0,0],
    [0,0,0,0,0,0,0,0,0],
    [7,2,0,0,0,0,0,0,0],
  ],
  evil: [
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [0,2,0,0,0,0,0,0,0],
    [0,0,0,5,0,0,4,0,7],
    [0,0,8,0,0,0,3,0,0],
    [1,0,0,0,0,9,0,0,0],
    [0,0,0,0,0,0,0,6,0],
    [0,0,0,0,0,0,0,0,0],
    [7,0,0,0,0,0,0,0,0],
  ],
};

function makeCell(r,c){
  const i = document.createElement('input');
  i.type='number'; i.min='0'; i.max='9'; i.dataset.r=r; i.dataset.c=c;
  i.addEventListener('input', ()=>{
    const v = parseInt(i.value||'0',10);
    i.value = v>=1 && v<=9 ? String(v) : '';
  });
  return i;
}
function renderGrid(){
  gridEl.innerHTML='';
  for(let r=0;r<9;r++) for(let c=0;c<9;c++) gridEl.appendChild(makeCell(r,c));
}
function getBoard(){
  const b = Array.from({length:9},()=>Array(9).fill(0));
  gridEl.querySelectorAll('input').forEach(inp=>{
    b[+inp.dataset.r][+inp.dataset.c] = parseInt(inp.value||'0',10) || 0;
  });
  return b;
}
function setBoard(b){
  gridEl.querySelectorAll('input').forEach(inp=>{
    const r=+inp.dataset.r,c=+inp.dataset.c; const v=b[r][c];
    inp.value = v ? String(v) : '';
  });
}
function loadSelected(){
  const diff = document.getElementById('difficulty').value;
  setBoard(PUZZLES[diff]);
}
async function solve(){
  msgEl.textContent = 'Solving…';
  try{
    const method = document.getElementById('method').value;
    const res = await fetch('/solve', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ board:getBoard(), method })
    });
    const data = await res.json();
    if(res.ok && data.solved){
      setBoard(data.board);
      msgEl.textContent = `Solved (${diffLabel()} / ${method}) in ${data.time_ms.toFixed(1)} ms · moves=${data.nodes}`;
    }else{
      msgEl.textContent = data.detail || data.message || 'No solution';
    }
  }catch(e){
    console.error(e);
    msgEl.textContent = 'Network error';
  }
}
function diffLabel(){ return document.getElementById('difficulty').value; }

document.getElementById('solveBtn').onclick = solve;
document.getElementById('clearBtn').onclick = ()=> setBoard(Array.from({length:9},()=>Array(9).fill(0)));
document.getElementById('loadBtn').onclick  = loadSelected;

renderGrid();
loadSelected(); // load default (easy) on start
