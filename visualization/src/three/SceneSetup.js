import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

export function createScene(canvas) {
    // ── renderer ───────────────────────────────────────────────────────────
    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: false,
    })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(canvas.clientWidth, canvas.clientHeight)
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type    = THREE.PCFSoftShadowMap
    renderer.toneMapping       = THREE.ACESFilmicToneMapping
    renderer.toneMappingExposure = 1.2

    // ── scene ──────────────────────────────────────────────────────────────
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x000000)
    scene.fog        = new THREE.FogExp2(0x000000, 0.018)

    // ── camera ─────────────────────────────────────────────────────────────
    const camera = new THREE.PerspectiveCamera(
        60,
        canvas.clientWidth / canvas.clientHeight,
        0.1,
        500
    )
    camera.position.set(25, 20, 25)
    camera.lookAt(7.5, 7.5, 7.5)   // center of a 15x15x15 maze

    // ── orbit controls ─────────────────────────────────────────────────────
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping    = true
    controls.dampingFactor    = 0.05
    controls.autoRotate       = true
    controls.autoRotateSpeed  = 0.4
    controls.minDistance      = 5
    controls.maxDistance      = 100
    controls.target.set(7.5, 7.5, 7.5)

    // ── lights ─────────────────────────────────────────────────────────────
    // ambient — base visibility
    const ambient = new THREE.AmbientLight(0x111122, 2.0)
    scene.add(ambient)

    // directional — main shadow caster
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.5)
    dirLight.position.set(20, 30, 20)
    dirLight.castShadow = true
    dirLight.shadow.mapSize.width  = 2048
    dirLight.shadow.mapSize.height = 2048
    scene.add(dirLight)

    // neon accent lights — sci-fi feel
    const neonBlue = new THREE.PointLight(0x00ffff, 3, 30)
    neonBlue.position.set(0, 15, 0)
    scene.add(neonBlue)

    const neonPurple = new THREE.PointLight(0x8800ff, 2, 25)
    neonPurple.position.set(15, 5, 15)
    scene.add(neonPurple)

    // ── resize handler ─────────────────────────────────────────────────────
    function onResize() {
        camera.aspect = canvas.clientWidth / canvas.clientHeight
        camera.updateProjectionMatrix()
        renderer.setSize(canvas.clientWidth, canvas.clientHeight)
    }
    window.addEventListener('resize', onResize)

    return { renderer, scene, camera, controls }
}
