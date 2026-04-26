import React from 'react'
import SceneCanvas from './components/SceneCanvas'

export default function App(){
  return (
    <div className="app-root">
      <SceneCanvas />
      <div className="ui-overlay">Voxel Gun Simulator (Prototype)</div>
    </div>
  )
}
