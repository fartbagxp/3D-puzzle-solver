import numpy as np
import time

def get_all_24_rotations():
    """Generate all 24 proper rotation matrices for a cube."""
    mats = []
    
    # Generate by composing basic rotations
    Rx90 = np.array([[1,0,0],[0,0,-1],[0,1,0]])
    Ry90 = np.array([[0,0,1],[0,1,0],[-1,0,0]])
    Rz90 = np.array([[0,-1,0],[1,0,0],[0,0,1]])
    
    # BFS over compositions
    queue = [np.eye(3, dtype=int)]
    seen = set()
    
    while queue:
        m = queue.pop(0)
        key = tuple(m.flatten())
        if key in seen:
            continue
        seen.add(key)
        mats.append(m)
        for basis in [Rx90, Ry90, Rz90]:
            new = (basis @ m).astype(int)
            if tuple(new.flatten()) not in seen:
                queue.append(new)
    
    return mats

mats = get_all_24_rotations()
print(f"Generated {len(mats)} rotation matrices")

# Verify with asymmetric piece
def normalize(voxels):
    arr = np.array(voxels)
    arr = arr - arr.min(axis=0)
    return tuple(sorted(map(tuple, arr.tolist())))

test = [(0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1)]
results = set()
for m in mats:
    rotated = [tuple((m @ np.array(v)).astype(int)) for v in test]
    results.add(normalize(rotated))
print(f"Asymmetric piece orientations: {len(results)} (should be 24)")

# Verify all dets = 1
dets = [int(round(np.linalg.det(m))) for m in mats]
print(f"All dets +1: {all(d==1 for d in dets)}")

# Now redo the full solve with correct rotations
pieces_raw = [
    [(0,1,0),(0,2,0),(0,3,0),(1,0,0),(1,1,0),(1,2,0),(2,0,0),(2,1,0),(3,0,0)],
    [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,1,1),(1,2,1),(2,1,1),(2,2,1)],
    [(0,0,0),(0,0,1),(0,1,0),(0,2,0),(0,3,0),(1,0,0)],
    [(0,0,0),(0,1,0),(0,2,0),(0,2,1),(1,1,0)],
    [(0,0,0),(0,1,0),(0,2,0),(1,0,0)],
    [(0,0,0),(1,0,0),(1,0,1),(1,1,1)],
    [(0,0,0),(0,1,0),(1,0,0),(0,1,1),(0,2,1)],
    [(0,0,0),(0,1,0),(1,0,0)],
    [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),(2,1,0)],
]

def normalize_piece(piece):
    arr = np.array(piece)
    arr = arr - arr.min(axis=0)
    return tuple(sorted(map(tuple, arr.tolist())))

def get_placements(piece):
    placements = set()
    seen_oris = set()
    for m in mats:
        rotated = [tuple((m @ np.array(v)).astype(int)) for v in piece]
        n = normalize_piece(rotated)
        if n in seen_oris:
            continue
        seen_oris.add(n)
        arr = np.array(n)
        mx = arr.max(axis=0)
        if mx[0] >= 5 or mx[1] >= 5 or mx[2] >= 2:
            continue
        for or_r in range(5 - mx[0]):
            for or_c in range(5 - mx[1]):
                for or_l in range(2 - mx[2]):
                    offset = np.array([or_r, or_c, or_l])
                    placed = frozenset(map(tuple, (arr + offset).tolist()))
                    placements.add(placed)
    return list(placements)

print("\nPrecomputing placements with correct 24 rotations...")
all_pls = []
for i, p in enumerate(pieces_raw):
    pl = get_placements(p)
    all_pls.append(pl)
    print(f"  Piece {i+1}: {len(pl)} placements")

ALL = frozenset((r,c,l) for r in range(5) for c in range(5) for l in range(2))
solutions = []

def solve(piece_set, occupied, placed):
    if len(solutions) > 3: return
    if not piece_set:
        if occupied == ALL:
            solutions.append(placed[:])
        return
    # first empty voxel
    target = None
    for l in range(2):
        for r in range(5):
            for c in range(5):
                if (r,c,l) not in occupied:
                    target = (r,c,l); break
            if target: break
        if target: break
    if not target: return
    
    for idx in list(piece_set):
        for pl in all_pls[idx]:
            if target in pl and not pl & occupied:
                placed.append((idx, pl))
                solve(piece_set - {idx}, occupied | pl, placed)
                placed.pop()

print("\nSolving...")
t0 = time.time()
solve(set(range(9)), frozenset(), [])
elapsed = time.time()-t0
print(f"Done in {elapsed:.2f}s. Solutions: {len(solutions)}")

def print_sol(sol, num):
    board = [[['.' for _ in range(2)] for _ in range(5)] for _ in range(5)]
    for idx, pl in sol:
        for r,c,l in pl:
            board[r][c][l] = str(idx+1)
    print(f"\n=== Solution {num} ===")
    for layer in range(2):
        print(f"  Layer {layer} ({'bottom' if layer==0 else 'top'}):")
        for row in range(5):
            print("    " + " ".join(board[row][col][layer] for col in range(5)))

for i, sol in enumerate(solutions):
    print_sol(sol, i+1)