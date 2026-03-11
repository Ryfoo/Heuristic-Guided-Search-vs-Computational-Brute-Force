import * as THREE from 'three'

// ── terrain colors (neon sci-fi palette) ───────────────────────────────────
const TERRAIN_COLORS = {
    1:  0x00ff88,   // grass  — neon green
    2:  0xffdd00,   // sand   — electric yellow
    4:  0x00aaff,   // water  — neon blue
    8:  0xff6600,   // mud    — neon orange
    10: 0xff0055,   // rock   — neon red
}

const WALL_COLOR    = 0x0a0a1a   // near-black dark blue
const START_COLOR   = 0x00ffff   // cyan
const GOAL_COLOR    = 0xff00ff   // magenta
const CELL_SIZE     = 1.0
const CELL_GAP      = 0.05       // small gap between cells for visibility

export class MazeRenderer {
    constructor(scene) {
        this.scene     = scene
        this.meshes    = []          // all cell meshes
        this.cellMap   = new Map()   // "x,y,z" → mesh
        this.group     = new THREE.Group()
        scene.add(this.group)
    }

    // ── build full maze from JSON data ─────────────────────────────────────
    build(mazeData) {
        this.clear()

        const { grid, width, height, depth, start, goal } = mazeData
        const size = CELL_SIZE - CELL_GAP

        // shared geometry for all cells — one geometry, many materials
        const geo = new THREE.BoxGeometry(size, size, size)

        for (let x = 0; x < width; x++) {
            for (let y = 0; y < height; y++) {
                for (let z = 0; z < depth; z++) {
                    const val = grid[x][y][z]

                    // skip walls — empty space reads as wall
                    if (val === 0) continue

                    const isStart = x === start[0] && y === start[1] && z === start[2]
                    const isGoal  = x === goal[0]  && y === goal[1]  && z === goal[2]

                    const color = isStart ? START_COLOR
                                : isGoal  ? GOAL_COLOR
                                : TERRAIN_COLORS[val] ?? 0x00ff88

                    const mat = new THREE.MeshStandardMaterial({
                        color,
                        emissive:         color,
                        emissiveIntensity: isStart || isGoal ? 0.8 : 0.15,
                        roughness:        0.4,
                        metalness:        0.3,
                        transparent:      true,
                        opacity:          0.92,
                    })

                    const mesh = new THREE.Mesh(geo, mat)
                    mesh.position.set(x, y, z)
                    mesh.castShadow    = true
                    mesh.receiveShadow = true

                    this.group.add(mesh)
                    this.meshes.push(mesh)
                    this.cellMap.set(`${x},${y},${z}`, mesh)
                }
            }
        }

        // center the maze in scene
        this.group.position.set(
            -width  / 2,
            -height / 2,
            -depth  / 2
        )
    }

    // ── highlight a single cell (used by animator) ─────────────────────────
    highlightCell(x, y, z, color, emissiveIntensity = 0.6) {
        const mesh = this.cellMap.get(`${x},${y},${z}`)
        if (!mesh) return
        mesh.material.color.setHex(color)
        mesh.material.emissive.setHex(color)
        mesh.material.emissiveIntensity = emissiveIntensity
    }

    // ── reset all cells to their original terrain color ────────────────────
    resetColors(mazeData) {
        const { grid, start, goal } = mazeData
        this.cellMap.forEach((mesh, key) => {
            const [x, y, z] = key.split(',').map(Number)
            const val       = grid[x][y][z]
            const isStart   = x === start[0] && y === start[1] && z === start[2]
            const isGoal    = x === goal[0]  && y === goal[1]  && z === goal[2]
            const color     = isStart ? START_COLOR
                            : isGoal  ? GOAL_COLOR
                            : TERRAIN_COLORS[val] ?? 0x00ff88
            mesh.material.color.setHex(color)
            mesh.material.emissive.setHex(color)
            mesh.material.emissiveIntensity = isStart || isGoal ? 0.8 : 0.15
        })
    }

    // ── clear all meshes ───────────────────────────────────────────────────
    clear() {
        this.meshes.forEach(m => {
            m.geometry.dispose()
            m.material.dispose()
            this.group.remove(m)
        })
        this.meshes  = []
        this.cellMap = new Map()
    }
}
