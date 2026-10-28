import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function BlochSphere3D({
  theta = 0,
  phi = 0,
}) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;

    if (!container) {
      return;
    }

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      45,
      container.clientWidth / container.clientHeight,
      0.1,
      100
    );

    camera.position.set(3.2, 2.4, 3.2);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
    });

    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(
      container.clientWidth,
      container.clientHeight
    );

    container.appendChild(renderer.domElement);

    const sphereGeometry = new THREE.SphereGeometry(
      1,
      32,
      32
    );

    const sphereMaterial = new THREE.MeshBasicMaterial({
      wireframe: true,
      opacity: 0.35,
      transparent: true,
    });

    const sphere = new THREE.Mesh(
      sphereGeometry,
      sphereMaterial
    );

    scene.add(sphere);

    const axesMaterial = new THREE.LineBasicMaterial();

    const axesGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-1.3, 0, 0),
      new THREE.Vector3(1.3, 0, 0),
    ]);

    const xAxis = new THREE.Line(
      axesGeometry,
      axesMaterial
    );

    scene.add(xAxis);

    const yGeometry =
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, -1.3, 0),
        new THREE.Vector3(0, 1.3, 0),
      ]);

    const yAxis = new THREE.Line(
      yGeometry,
      axesMaterial
    );

    scene.add(yAxis);

    const zGeometry =
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, -1.3),
        new THREE.Vector3(0, 0, 1.3),
      ]);

    const zAxis = new THREE.Line(
      zGeometry,
      axesMaterial
    );

    scene.add(zAxis);

    const phiRadians = Number(phi);
    const thetaRadians = Number(theta);

    const x =
      Math.sin(thetaRadians) *
      Math.cos(phiRadians);

    const y =
      Math.sin(thetaRadians) *
      Math.sin(phiRadians);

    const z = Math.cos(thetaRadians);

    const vectorGeometry =
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(x, y, z),
      ]);

    const vectorMaterial =
      new THREE.LineBasicMaterial();

    const stateVector = new THREE.Line(
      vectorGeometry,
      vectorMaterial
    );

    scene.add(stateVector);

    const pointGeometry =
      new THREE.SphereGeometry(0.07, 16, 16);

    const pointMaterial =
      new THREE.MeshBasicMaterial();

    const statePoint = new THREE.Mesh(
      pointGeometry,
      pointMaterial
    );

    statePoint.position.set(x, y, z);

    scene.add(statePoint);

    function handleResize() {
      if (!container) {
        return;
      }

      const width = container.clientWidth;
      const height = container.clientHeight;

      camera.aspect = width / height;
      camera.updateProjectionMatrix();

      renderer.setSize(width, height);
    }

    window.addEventListener(
      "resize",
      handleResize
    );

    let animationFrameId;

    function animate() {
      animationFrameId =
        requestAnimationFrame(animate);

      sphere.rotation.y += 0.002;

      renderer.render(
        scene,
        camera
      );
    }

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);

      window.removeEventListener(
        "resize",
        handleResize
      );

      renderer.dispose();

      if (
        renderer.domElement &&
        container.contains(renderer.domElement)
      ) {
        container.removeChild(
          renderer.domElement
        );
      }
    };
  }, [theta, phi]);

  return (
    <div
      ref={containerRef}
      className="bloch-3d-container"
    />
  );
}
