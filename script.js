let scene, camera, renderer, leftPanel, rightPanel;

init();
animate();

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 2;

    renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas') });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const geometry = new THREE.PlaneGeometry(1, 2);
    const material = new THREE.MeshBasicMaterial({ color: 0x1c1c1c, side: THREE.DoubleSide });

    leftPanel = new THREE.Mesh(geometry, material);
    rightPanel = new THREE.Mesh(geometry, material);

    leftPanel.position.x = -0.5;
    rightPanel.position.x = 0.5;

    scene.add(leftPanel);
    scene.add(rightPanel);

    window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function unfoldPanels() {
    new TWEEN.Tween(leftPanel.rotation)
        .to({ y: Math.PI / 2 }, 2000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .start();

    new TWEEN.Tween(rightPanel.rotation)
        .to({ y: -Math.PI / 2 }, 2000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .start();
}

function animate() {
    requestAnimationFrame(animate);
    TWEEN.update();
    renderer.render(scene, camera);
}

function openBrochure() {
    unfoldPanels();
}
