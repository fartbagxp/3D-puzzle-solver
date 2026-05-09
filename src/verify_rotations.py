# Verify rotation matrices are correct by checking they form a group
# and produce exactly 24 distinct orientations for an asymmetric piece
import numpy as np

ROT_MATRICES=[[[1,0,0],[0,1,0],[0,0,1]],[[1,0,0],[0,0,-1],[0,1,0]],[[1,0,0],[0,-1,0],[0,0,-1]],[[1,0,0],[0,0,1],[0,-1,0]],[[-1,0,0],[0,-1,0],[0,0,1]],[[-1,0,0],[0,0,-1],[0,-1,0]],[[-1,0,0],[0,1,0],[0,0,-1]],[[-1,0,0],[0,0,1],[0,1,0]],[[0,1,0],[-1,0,0],[0,0,1]],[[0,1,0],[0,0,-1],[-1,0,0]],[[0,1,0],[1,0,0],[0,0,-1]],[[0,1,0],[0,0,1],[1,0,0]],[[0,-1,0],[1,0,0],[0,0,1]],[[0,-1,0],[0,0,1],[-1,0,0]],[[0,-1,0],[-1,0,0],[0,0,-1]],[[0,-1,0],[0,0,-1],[1,0,0]],[[0,0,1],[0,1,0],[-1,0,0]],[[0,0,1],[1,0,0],[0,1,0]],[[0,0,1],[0,-1,0],[1,0,0]],[[0,0,1],[-1,0,0],[0,-1,0]],[[0,0,-1],[0,1,0],[1,0,0]],[[0,0,-1],[-1,0,0],[0,1,0]],[[0,0,-1],[0,-1,0],[-1,0,0]],[[0,0,-1],[1,0,0],[0,-1,0]]]

mats = [np.array(m) for m in ROT_MATRICES]

# Check: all determinants should be +1 (proper rotations)
dets = [int(round(np.linalg.det(m))) for m in mats]
print(f"All determinants +1: {all(d==1 for d in dets)} (dets: {set(dets)})")

# Check: applying all 24 rotations to an asymmetric piece gives 24 distinct results
def normalize(voxels):
    arr = np.array(voxels)
    arr = arr - arr.min(axis=0)
    return tuple(sorted(map(tuple, arr.tolist())))

test_piece = [(0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1)]  # asymmetric
results = set()
for m in mats:
    rotated = [tuple(m @ np.array(v)) for v in test_piece]
    results.add(normalize(rotated))

print(f"Distinct orientations of asymmetric piece: {len(results)} (should be 24)")

# Now test with piece 2 specifically
p2 = [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,1,1),(1,2,1),(2,1,1),(2,2,1)]

def normalize_p(voxels):
    arr = np.array(voxels)
    mn = arr.min(axis=0)
    arr = arr - mn
    return tuple(sorted(map(tuple, arr.tolist())))

p2_orientations = set()
for m in mats:
    rotated = [tuple((m @ np.array(v)).astype(int)) for v in p2]
    p2_orientations.add(normalize_p(rotated))

print(f"\nPiece 2 distinct orientations: {len(p2_orientations)}")

# For each orientation, check if it fits in 5x5x2
valid = []
for ori in p2_orientations:
    arr = np.array(ori)
    mx = arr.max(axis=0)
    if mx[0] < 5 and mx[1] < 5 and mx[2] < 2:
        l0 = sum(1 for v in ori if v[2]==0)
        l1 = sum(1 for v in ori if v[2]==1)
        valid.append((l0, l1, ori))

print(f"Valid orientations of piece 2 (fit in 5x5x2): {len(valid)}")
for l0,l1,ori in valid:
    print(f"  l0={l0}, l1={l1}: {sorted(ori)}")