import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { createScene }   from '../three/SceneSetup'
import { MazeRenderer }  from '../three/MazeRenderer'
import { SearchAnimator } from '../three/SearchAnimator'
import { useMazeData }   from '../hooks/useMazeData'

const ALGO_COLORS = {
    bfs:   '#00ffff',
    astar: '#ff00ff',
}

const MAZE_SIZES = [
    { label: '10×10×10', file: '/data/maze_3d_10x10x10.json' },
    { label: '20×20×20', file: '/data/maze_3d_20x20x20.json' },
    { label: '50×50×50', file: '/data/maze_3d_50x50x50.json' },
    { label: '100×100×100', file: '/data/maze_3d_100x100x100.json' },
]


export default function Maze3DViewer() {
    const canvasRef   = useRef(null)
    const rendererRef = useRef(null)
    const animRef     = useRef(null)
    const mazeRef     = useRef(null)
    const sceneRef    = useRef(null)

    const [algo,     setAlgo]     = useState('bfs')
    const [playing,  setPlaying]  = useState(false)
    const [progress, setProgress] = useState(0)
    const [speed,    setSpeed]    = useState(8)
    const [complete, setComplete] = useState(false)
    const [selectedSize, setSelectedSize] = useState(MAZE_SIZES[0].file)
    const { data, loading, error } = useMazeData(selectedSize)


    // ── initialize Three.js once ───────────────────────────────────────────
    useEffect(() => {
        if (!canvasRef.current) return

        const { renderer, scene, camera, controls } = createScene(canvasRef.current)
        const mazeRenderer = new MazeRenderer(scene)
        const animator     = new SearchAnimator(mazeRenderer)

        sceneRef.current   = { renderer, scene, camera, controls }
        mazeRef.current    = mazeRenderer
        animRef.current    = animator

        // render loop
        let frameId
        function animate() {
            frameId = requestAnimationFrame(animate)
            animator.tick()
            setProgress(animator.progress)
            controls.update()
            renderer.render(scene, camera)
        }
        animate()

        return () => {
            cancelAnimationFrame(frameId)
            renderer.dispose()
        }
    }, [])

    // ── load maze data when JSON is ready ──────────────────────────────────
    useEffect(() => {
        if (!data || !mazeRef.current || !animRef.current) return
        mazeRef.current.build(data.maze)
        loadAlgo(algo)
    }, [data])

    // ── switch algorithm ───────────────────────────────────────────────────
    function loadAlgo(name) {
        if (!data || !animRef.current) return
        const algoData = data.algorithms[name]
        if (!algoData) return
        animRef.current.load(data.maze, algoData)
        animRef.current.setSpeed(speed)
        animRef.current.onComplete = () => setComplete(true)
        setPlaying(false)
        setProgress(0)
        setComplete(false)
    }

    function handleAlgoSwitch(name) {
        setAlgo(name)
        loadAlgo(name)
    }

    function handlePlay() {
        if (!animRef.current) return
        if (complete) {
            animRef.current.reset()
            loadAlgo(algo)
            setComplete(false)
        }
        animRef.current.play()
        setPlaying(true)
    }

    function handlePause() {
        if (!animRef.current) return
        animRef.current.pause()
        setPlaying(false)
    }

    function handleReset() {
        if (!animRef.current) return
        animRef.current.reset()
        setPlaying(false)
        setProgress(0)
        setComplete(false)
    }

    function handleSpeed(e) {
        const v = Number(e.target.value)
        setSpeed(v)
        if (animRef.current) animRef.current.setSpeed(v)
    }

    if (loading) return <div style={styles.status}>Loading maze data...</div>
    if (error)   return <div style={styles.status}>Error: {error}</div>

    const algoData = data?.algorithms[algo]

    return (
        <div style={styles.container}>

            {/* ── canvas ─────────────────────────────────────────── */}
            <canvas ref={canvasRef} style={styles.canvas} />

            {/* ── overlay UI ─────────────────────────────────────── */}
            <div style={styles.overlay}>

                {/* title */}
                <div style={styles.title}>
                    3D MAZE SEARCH
                    <span style={{ color: ALGO_COLORS[algo], marginLeft: 12 }}>
                        {algo.toUpperCase()}
                    </span>
                </div>

                {/* algorithm selector */}
                <div style={styles.algoRow}>
                    {Object.keys(data?.algorithms || {}).map(name => (
                        <button
                            key={name}
                            onClick={() => handleAlgoSwitch(name)}
                            style={{
                                ...styles.algoBtn,
                                borderColor: ALGO_COLORS[name] || '#fff',
                                color:       algo === name ? '#000' : ALGO_COLORS[name] || '#fff',
                                background:  algo === name ? (ALGO_COLORS[name] || '#fff') : 'transparent',
                            }}
                        >
                            {name.toUpperCase()}
                        </button>
                    ))}
                </div>
                <div style={styles.sizeRow}>
                    {MAZE_SIZES.map(({ label, file }) => (
                        <button
                            key={file}
                            onClick={() => setSelectedSize(file)}
                            style={{
                                ...styles.algoBtn,
                                borderColor: selectedSize === file ? '#aa44ff' : '#1a1a3a',
                                color:       selectedSize === file ? '#aa44ff' : '#333366',
                                background:  'transparent',
                            }}
                        >
                            {label}
                        </button>
                    ))}
                </div>
                {/* stats */}
                {algoData && (
                    <div style={styles.stats}>
                        <span>Nodes: <b style={{ color: ALGO_COLORS[algo] }}>{algoData.nodes_expanded}</b></span>
                        <span>Path:  <b style={{ color: '#ffff00' }}>{algoData.path_length}</b></span>
                        <span>Time:  <b style={{ color: '#ffffff' }}>{algoData.runtime}s</b></span>
                    </div>
                )}

                {/* progress bar */}
                <div style={styles.progressBar}>
                    <div style={{
                        ...styles.progressFill,
                        width:      `${progress * 100}%`,
                        background: ALGO_COLORS[algo] || '#00ffff',
                    }} />
                </div>

                {/* controls */}
                <div style={styles.controls}>
                    <button onClick={handlePlay}  style={styles.btn} disabled={playing && !complete}>▶ Play</button>
                    <button onClick={handlePause} style={styles.btn} disabled={!playing}>⏸ Pause</button>
                    <button onClick={handleReset} style={styles.btn}>↺ Reset</button>
                </div>

                {/* speed */}
                <div style={styles.speedRow}>
                    <span style={{ color: '#888', fontSize: 11 }}>SPEED</span>
                    <input
                        type="range" min={1} max={50} value={speed}
                        onChange={handleSpeed}
                        style={{ width: 100, accentColor: ALGO_COLORS[algo] }}
                    />
                    <span style={{ color: '#ccc', fontSize: 11 }}>{speed}x</span>
                </div>

                {/* legend */}
                <div style={styles.legend}>
                    {[
                        ['#00ffff', 'Start'],
                        ['#ff00ff', 'Goal'],
                        ['#4444ff', 'Explored'],
                        ['#00ffff', 'Frontier'],
                        ['#ffff00', 'Path'],
                    ].map(([color, label]) => (
                        <div key={label} style={styles.legendItem}>
                            <div style={{ ...styles.legendDot, background: color }} />
                            <span>{label}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

// ── styles ─────────────────────────────────────────────────────────────────
const styles = {
    container: {
        position:   'relative',
        width:      '100%',
        height:     '100vh',
        background: '#000',
        fontFamily: "'Courier New', monospace",
    },
    canvas: {
        width:  '100%',
        height: '100%',
        display: 'block',
    },
    overlay: {
        position:  'absolute',
        top:       20,
        left:      20,
        display:   'flex',
        flexDirection: 'column',
        gap:       10,
    },
    title: {
        color:      '#fff',
        fontSize:   18,
        fontWeight: 'bold',
        letterSpacing: 3,
        textTransform: 'uppercase',
    },
    algoRow: {
        display: 'flex',
        gap: 8,
    },
    algoBtn: {
        padding:      '4px 12px',
        border:       '1px solid',
        borderRadius: 2,
        cursor:       'pointer',
        fontSize:     11,
        fontFamily:   "'Courier New', monospace",
        letterSpacing: 2,
        transition:   'all 0.2s',
    },
    stats: {
        display:    'flex',
        gap:        16,
        color:      '#888',
        fontSize:   12,
        letterSpacing: 1,
    },
    progressBar: {
        width:        220,
        height:       3,
        background:   '#111',
        borderRadius: 2,
        overflow:     'hidden',
    },
    progressFill: {
        height:     '100%',
        transition: 'width 0.1s linear',
    },
    controls: {
        display: 'flex',
        gap:     8,
    },
    btn: {
        padding:      '5px 12px',
        background:   'transparent',
        border:       '1px solid #333',
        color:        '#ccc',
        cursor:       'pointer',
        fontSize:     11,
        fontFamily:   "'Courier New', monospace",
        letterSpacing: 1,
        borderRadius: 2,
    },
    speedRow: {
        display:    'flex',
        alignItems: 'center',
        gap:        8,
    },
    legend: {
        display:       'flex',
        flexDirection: 'column',
        gap:           4,
        marginTop:     4,
    },
    legendItem: {
        display:    'flex',
        alignItems: 'center',
        gap:        6,
        color:      '#666',
        fontSize:   11,
        letterSpacing: 1,
    },
    legendDot: {
        width:        8,
        height:       8,
        borderRadius: '50%',
    },
    status: {
        color:      '#00ffff',
        fontFamily: "'Courier New', monospace",
        padding:    40,
        fontSize:   14,
    },
}
