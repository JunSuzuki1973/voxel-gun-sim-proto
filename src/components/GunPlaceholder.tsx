import React from 'react'
import { Mesh } from 'three'

export default function GunPlaceholder(){
  return (
    <mesh position={[0,0,0]}>
      <boxGeometry args={[2,0.5,0.5]} />
      <meshStandardMaterial color="#555" />
    </mesh>
  )
}
