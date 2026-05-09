const PIECE_COLORS = {
  1: '#C17F50',
  2: '#7F77DD',
  3: '#5CAF6F',
  4: '#D06070',
  5: '#5A9EC9',
  6: '#C8A83D',
  7: '#8D6AB8',
  8: '#7CA87C',
  9: '#C07070',
};

const pieces = [
  { name: 'Piece 1 — fish', sub: '9 voxels, bottom layer only',
    voxels: [[0,1,0],[0,2,0],[0,3,0],[1,0,0],[1,1,0],[1,2,0],[2,0,0],[2,1,0],[3,0,0]] },
  { name: 'Piece 2 — two squares', sub: '8 voxels, 4 bottom + 4 top',
    voxels: [[0,0,0],[0,1,0],[1,0,0],[1,1,0],[1,1,1],[1,2,1],[2,1,1],[2,2,1]] },
  { name: 'Piece 3', sub: '6 voxels, 5 bottom + 1 top',
    voxels: [[0,0,0],[0,0,1],[0,1,0],[0,2,0],[0,3,0],[1,0,0]] },
  { name: 'Piece 4', sub: '5 voxels, 4 bottom + 1 top',
    voxels: [[0,0,0],[0,1,0],[0,2,0],[0,2,1],[1,1,0]] },
  { name: 'Piece 5', sub: '4 voxels, bottom layer only',
    voxels: [[0,0,0],[0,1,0],[0,2,0],[1,0,0]] },
  { name: 'Piece 6', sub: '4 voxels, 2 bottom + 2 top',
    voxels: [[0,0,0],[1,0,0],[1,0,1],[1,1,1]] },
  { name: 'Piece 7', sub: '5 voxels, 3 bottom + 2 top',
    voxels: [[0,0,0],[0,1,0],[1,0,0],[0,1,1],[0,2,1]] },
  { name: 'Piece 8', sub: '3 voxels, bottom layer only',
    voxels: [[0,0,0],[0,1,0],[1,0,0]] },
  { name: 'Piece 9', sub: '6 voxels, bottom layer only',
    voxels: [[0,0,0],[0,1,0],[1,0,0],[1,1,0],[1,2,0],[2,1,0]] },
];

const solutions = [
  {
    title: 'Solution 1',
    bottom: [[1,1,1,5,4],[7,1,1,1,3],[7,7,1,1,3],[6,2,2,1,3],[6,2,2,3,3]],
    top:    [[7,5,5,5,4],[7,8,8,4,4],[2,2,8,9,4],[2,2,9,9,9],[6,6,9,9,3]],
  },
  {
    title: 'Solution 2',
    bottom: [[3,1,1,1,7],[1,1,1,4,4],[1,1,2,2,4],[1,6,2,2,4],[6,6,5,5,5]],
    top:    [[3,3,3,3,7],[3,8,8,7,7],[9,9,8,7,4],[9,9,9,2,2],[6,9,5,2,2]],
  },
];

function makeVoxelGrid(voxels, layer) {
  const occupied = new Set(
    voxels.filter(v => v[2] === layer).map(v => `${v[0]},${v[1]}`)
  );
  const grid = document.createElement('div');
  grid.className = 'voxel-grid';
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 5; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (occupied.has(`${r},${c}`)) {
        const pieceNum = layer === 0 ? 1 : 2; // unused here; color is per piece
        cell.style.background = layer === 0 ? '#C17F50' : '#7F77DD';
      }
      grid.appendChild(cell);
    }
  }
  return grid;
}

function makePieceVoxelGrid(voxels, layer, pieceColor) {
  const occupied = new Set(
    voxels.filter(v => v[2] === layer).map(v => `${v[0]},${v[1]}`)
  );
  const grid = document.createElement('div');
  grid.className = 'voxel-grid';
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 5; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (occupied.has(`${r},${c}`)) {
        cell.style.background = layer === 0 ? '#C17F50' : '#7F77DD';
      }
      grid.appendChild(cell);
    }
  }
  return grid;
}

function makeSolutionGrid(layer5x5) {
  const grid = document.createElement('div');
  grid.className = 'solution-grid';
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 5; c++) {
      const p = layer5x5[r][c];
      const cell = document.createElement('div');
      cell.className = 'solution-cell';
      cell.style.background = PIECE_COLORS[p];
      cell.textContent = p;
      grid.appendChild(cell);
    }
  }
  return grid;
}

// Render pieces
const pieceContainer = document.getElementById('pieces');
pieces.forEach((p, idx) => {
  const card = document.createElement('div');
  card.className = 'piece-card';

  const name = document.createElement('div');
  name.className = 'piece-name';
  name.style.color = PIECE_COLORS[idx + 1];
  name.textContent = p.name;
  card.appendChild(name);

  const sub = document.createElement('div');
  sub.className = 'piece-sub';
  sub.textContent = p.sub;
  card.appendChild(sub);

  const row = document.createElement('div');
  row.className = 'layer-row';

  [0, 1].forEach(layer => {
    const col = document.createElement('div');
    col.className = 'layer-col';
    const label = document.createElement('div');
    label.className = 'layer-label';
    label.textContent = layer === 0 ? 'bottom' : 'top';
    col.appendChild(label);
    col.appendChild(makePieceVoxelGrid(p.voxels, layer, PIECE_COLORS[idx + 1]));
    row.appendChild(col);
  });

  card.appendChild(row);
  pieceContainer.appendChild(card);
});

// Render legend
const legend = document.getElementById('legend');
pieces.forEach((p, idx) => {
  const item = document.createElement('div');
  item.className = 'legend-item';
  const swatch = document.createElement('div');
  swatch.className = 'legend-swatch';
  swatch.style.background = PIECE_COLORS[idx + 1];
  item.appendChild(swatch);
  item.appendChild(document.createTextNode(`Piece ${idx + 1}`));
  legend.appendChild(item);
});

// Render solutions
const solutionsContainer = document.getElementById('solutions');
solutions.forEach(sol => {
  const block = document.createElement('div');
  block.className = 'solution-block';

  const title = document.createElement('div');
  title.className = 'solution-title';
  title.textContent = sol.title;
  block.appendChild(title);

  const pair = document.createElement('div');
  pair.className = 'solution-pair';

  ['bottom', 'top'].forEach(layerKey => {
    const col = document.createElement('div');
    col.className = 'solution-layer';
    const label = document.createElement('div');
    label.className = 'solution-layer-label';
    label.textContent = layerKey === 'bottom' ? 'Bottom layer' : 'Top layer';
    col.appendChild(label);
    col.appendChild(makeSolutionGrid(sol[layerKey]));
    pair.appendChild(col);
  });

  block.appendChild(pair);
  solutionsContainer.appendChild(block);
});
