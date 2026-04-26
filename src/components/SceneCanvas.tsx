import React from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import GunPlaceholder from './GunPlaceholder'

export default function SceneCanvas(){
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 10, 7]} intensity={0.8} />
      <GunPlaceholder />
      <OrbitControls />
    </Canvas>
  )
}
