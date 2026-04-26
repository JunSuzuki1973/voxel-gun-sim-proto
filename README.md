<<<<<<< HEAD
プロジェクト: モデルガン分解組み立てシミュレーター（プロトタイプ）
方針: B — React Three Fiber + TypeScript + @react-spring（拡張性重視）
目的: 今回は各LLMのコーディング出力性能を評価するための実装雛形を自動生成します。

セットアップ:
1. cd prototype/bootstrap
2. npm install
3. npm run dev

生成物:
- package.json
- tsconfig.json
- vite.config.ts
- index.html
- src/main.tsx
- src/App.tsx
- src/components/SceneCanvas.tsx
- src/components/GunPlaceholder.tsx
- src/styles.css

注記: これは最小限のブートストラップです。ボクセルガンモデル等は含みません。テスト目的でのコード生成品質と互換性を早期に確認するための雛形です。
=======
# Voxel Gun Disassembly/Assembly Simulator

A Python program that allows users to load a voxel-based gun model, disassemble it into parts, and reassemble it. The program uses a simple 3D array representation for voxels and provides a graphical interface using PyGame.

## Features

- Load voxel-based gun models
- Disassemble and reassemble gun parts
- Basic controls: select part, move, rotate, attach/detach
- Sample voxel data for a simple pistol with barrel, slide, frame, magazine, and trigger
- Interactive 3D visualization with camera controls
- Part selection and manipulation

## Requirements

- Python 3.6+
- PyGame
- NumPy

## Installation

The required dependencies can be installed using pip:

```bash
pip install pygame numpy
```

Or on Debian/Ubuntu systems:

```bash
sudo apt-get install python3-pygame python3-numpy
```

## Usage

To run the simulator:

```bash
python voxel_gun_simulator.py
```

## Controls

### Camera Movement:
- WASD: Move camera horizontally and vertically
- Q/E: Move camera up/down
- Arrow Keys: Rotate camera
- Page Up/Down: Zoom in/out
- Space: Reset camera view

### Part Selection:
- 1: Select Barrel
- 2: Select Slide
- 3: Select Frame
- 4: Select Magazine
- 5: Select Trigger

### Selected Part Manipulation:
- I/J/K/L: Move part in X/Y/Z directions
- U/O: Move part up/down
- T/G: Rotate part around X-axis
- F/H: Rotate part around Y-axis
- Y/C: Rotate part around Z-axis

### Interface:
- ESC: Quit the application
- On-screen instructions show current controls and selected part

## Code Structure

The simulator consists of several classes:

- `PartType`: Enumeration of different gun part types
- `VoxelPart`: Represents a single part of the gun as a 3D array of voxels
- `GunModel`: Represents the complete gun model composed of multiple parts
- `Camera`: Handles camera positioning and orientation in 3D space
- `VoxelRenderer`: Renders the 3D voxel models to the screen
- `create_sample_pistol()`: Function that creates a sample pistol model with basic parts

## Technical Details

- Voxels are represented as 3D arrays of binary values (1 for occupied, 0 for empty)
- Each part has its own position and rotation in 3D space
- Colors are assigned to each part type for visual distinction
- The renderer implements a simple perspective projection for 3D visualization
- Input handling supports both discrete key presses and continuous key presses for smooth movement

## Sample Model

The default model is a simplified pistol with 5 main components:
1. Barrel: The tube through which the projectile travels
2. Slide: The reciprocating part that cycles ammunition
3. Frame: The main body that holds all components
4. Magazine: Holds ammunition ready for firing
5. Trigger: Mechanical component for firing

Each component is represented with a different color and appropriate dimensions for visual identification.
>>>>>>> 1dd587e (Add full workspace files including dist)
