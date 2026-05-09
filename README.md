# Otaku Baz 3D Puzzle Solver

A brute-force solver for the [Otaku Baz Puzzle](https://baz.llc/products/otaku-baz) — a handcrafted 5×5×2 polycube packing puzzle. After spending many hours trying to solve it by hand, I wrote a solver.

**Live visualization:** [fartbagxp.github.io/3D-puzzle-solver](https://fartbagxp.github.io/3D-puzzle-solver).

## The Puzzle

The tray is **5 wide × 5 deep × 2 tall = 50 unit voxels**. Nine wooden pieces, each a unique 3D polycube shape, must fill the tray completely. According to the manufacturer, there are exactly two solutions.

### The 9 Pieces

Each piece is described as a list of `(row, col, layer)` voxel coordinates, where layer `0` is the bottom and layer `1` is the top.

| #   | Voxels                                                                    |
| --- | ------------------------------------------------------------------------- |
| 1   | `(0,1,0),(0,2,0),(0,3,0),(1,0,0),(1,1,0),(1,2,0),(2,0,0),(2,1,0),(3,0,0)` |
| 2   | `(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,1,1),(1,2,1),(2,1,1),(2,2,1)`         |
| 3   | `(0,0,0),(0,0,1),(0,1,0),(0,2,0),(0,3,0),(1,0,0)`                         |
| 4   | `(0,0,0),(0,1,0),(0,2,0),(0,2,1),(1,1,0)`                                 |
| 5   | `(0,0,0),(0,1,0),(0,2,0),(1,0,0)`                                         |
| 6   | `(0,0,0),(1,0,0),(1,0,1),(1,1,1)`                                         |
| 7   | `(0,0,0),(0,1,0),(1,0,0),(0,1,1),(0,2,1)`                                 |
| 8   | `(0,0,0),(0,1,0),(1,0,0)`                                                 |
| 9   | `(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),(2,1,0)`                         |

## Approach

The solver uses **exhaustive backtracking** with precomputed placements:

1. **Generate all 24 proper 3D rotation matrices** via BFS over three 90° basis rotations (around X, Y, Z axes). Using BFS ensures all 24 are found — a naive approach only finds 12 and misses solutions entirely.
2. **Precompute all valid placements** for each piece: apply every rotation, deduplicate by normalized shape, then enumerate every (row, col, layer) offset that keeps the piece inside the 5×5×2 bounds.
3. **Backtrack**: always target the first unoccupied voxel, try every piece/placement that covers it, recurse. Stops after finding 4 solutions (which collapse to 2 distinct ones under the puzzle's symmetry).

The solver finds all solutions in a few seconds.

## Running

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
# Verify the 24 rotation matrices are correct
uv run python src/verify_rotations.py

# Run the solver and print both solutions
uv run python src/solve_rotations.py
```
