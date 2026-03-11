import * as THREE from 'three'

// ── animation colors ───────────────────────────────────────────────────────
const VISITED_COLOR  = 0x4444ff   // dim blue — explored but not on path
const FRONTIER_COLOR = 0x00ffff   // bright cyan — current frontier
const PATH_COLOR     = 0xffff00   // yellow — final path

export class SearchAnimator {
    constructor(mazeRenderer) {
        this.renderer   = mazeRenderer
        this.mazeData   = null
        this.algoData   = null

        this.visitedOrder = []
        this.path         = []

        this.currentStep  = 0
        this.isPlaying    = false
        this.isComplete   = false
        this.speed        = 5        // cells highlighted per frame
        this.onComplete   = null     // callback when animation ends
    }

    // ── load algorithm data ────────────────────────────────────────────────
    load(mazeData, algoData) {
        this.mazeData     = mazeData
        this.algoData     = algoData
        this.visitedOrder = algoData.visited_order || []
        this.path         = algoData.path || []
        this.currentStep  = 0
        this.isComplete   = false
        this.isPlaying    = false
        this.renderer.resetColors(mazeData)
    }

    // ── playback controls ──────────────────────────────────────────────────
    play()   { this.isPlaying = true  }
    pause()  { this.isPlaying = false }
    reset()  {
        this.currentStep = 0
        this.isComplete  = false
        this.isPlaying   = false
        if (this.mazeData) this.renderer.resetColors(this.mazeData)
    }

    setSpeed(speed) { this.speed = Math.max(1, speed) }

    // ── tick — call this every frame from the render loop ─────────────────
    tick() {
        if (!this.isPlaying || this.isComplete) return

        const end = Math.min(
            this.currentStep + this.speed,
            this.visitedOrder.length
        )

        for (let i = this.currentStep; i < end; i++) {
            const [x, y, z] = this.visitedOrder[i]
            this.renderer.highlightCell(x, y, z, VISITED_COLOR, 0.4)
        }

        // highlight the latest batch as frontier (brighter)
        if (end > 0) {
            const [fx, fy, fz] = this.visitedOrder[end - 1]
            this.renderer.highlightCell(fx, fy, fz, FRONTIER_COLOR, 0.9)
        }

        this.currentStep = end

        // animation complete — draw path
        if (this.currentStep >= this.visitedOrder.length) {
            this._drawPath()
            this.isComplete = true
            this.isPlaying  = false
            if (this.onComplete) this.onComplete()
        }
    }

    // ── draw final path ────────────────────────────────────────────────────
    _drawPath() {
        this.path.forEach(([x, y, z]) => {
            this.renderer.highlightCell(x, y, z, PATH_COLOR, 1.0)
        })
    }

    // ── progress 0..1 ─────────────────────────────────────────────────────
    get progress() {
        if (!this.visitedOrder.length) return 0
        return this.currentStep / this.visitedOrder.length
    }
}
