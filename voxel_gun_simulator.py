#!/usr/bin/env python3
"""
Voxel Gun Disassembly/Assembly Simulator

A program that allows users to load a voxel-based gun model, disassemble it into parts,
and reassemble it. Uses a 3D array representation for voxels and provides a
graphical interface using pygame.

Features:
- Load voxel-based gun models
- Disassemble and reassemble gun parts
- Basic controls: select part, move, rotate, attach/detach
- Sample voxel data for a simple pistol with barrel, slide, frame, magazine
"""

import pygame
import numpy as np
import sys
from enum import Enum
from typing import Dict, List, Tuple, Optional


class PartType(Enum):
    BARREL = "barrel"
    SLIDE = "slide"
    FRAME = "frame"
    MAGAZINE = "magazine"
    TRIGGER = "trigger"


class VoxelPart:
    """
    Represents a single part of the gun as a 3D array of voxels
    """

    def __init__(
        self,
        name: str,
        part_type: PartType,
        voxels: np.ndarray,
        color: Tuple[int, int, int],
    ):
        """
        Initialize a voxel part

        Args:
            name: Name of the part
            part_type: Type of the part (BARREL, SLIDE, etc.)
            voxels: 3D numpy array representing the voxels (1 for occupied, 0 for empty)
            color: RGB color tuple for this part
        """
        self.name = name
        self.part_type = part_type
        self.voxels = voxels  # 3D array of 0s and 1s
        self.color = color
        self.position = np.array([0, 0, 0])  # Current position in 3D space
        self.rotation = np.array([0, 0, 0])  # Rotation angles around x, y, z axes
        self.attached_to: Optional["VoxelPart"] = None  # Part this is attached to
        self.attached_parts: List["VoxelPart"] = []  # Parts attached to this

    def get_size(self) -> Tuple[int, int, int]:
        """Get the dimensions of the voxel grid"""
        return self.voxels.shape

    def get_position(self) -> np.ndarray:
        """Get the current position of the part"""
        return self.position.copy()

    def set_position(self, pos: np.ndarray):
        """Set the position of the part"""
        self.position = pos.copy()

    def get_rotation(self) -> np.ndarray:
        """Get the current rotation of the part"""
        return self.rotation.copy()

    def set_rotation(self, rot: np.ndarray):
        """Set the rotation of the part"""
        self.rotation = rot.copy()

    def move(self, delta: np.ndarray):
        """Move the part by a delta vector"""
        self.position += delta

    def rotate(self, delta: np.ndarray):
        """Rotate the part by a delta vector"""
        self.rotation += delta


class GunModel:
    """
    Represents the complete gun model composed of multiple parts
    """

    def __init__(self, name: str):
        self.name = name
        self.parts: Dict[str, VoxelPart] = {}
        self.selected_part: Optional[VoxelPart] = None

    def add_part(self, part: VoxelPart):
        """Add a part to the gun model"""
        self.parts[part.name] = part

    def remove_part(self, part_name: str):
        """Remove a part from the gun model"""
        if part_name in self.parts:
            del self.parts[part_name]

    def get_part(self, part_name: str) -> Optional[VoxelPart]:
        """Get a part by name"""
        return self.parts.get(part_name)

    def get_all_parts(self) -> List[VoxelPart]:
        """Get all parts in the model"""
        return list(self.parts.values())

    def select_part(self, part_name: str):
        """Select a part by name"""
        if part_name in self.parts:
            self.selected_part = self.parts[part_name]

    def get_selected_part(self) -> Optional[VoxelPart]:
        """Get the currently selected part"""
        return self.selected_part

    def attach_parts(self, part1_name: str, part2_name: str):
        """Attach two parts together"""
        part1 = self.parts.get(part1_name)
        part2 = self.parts.get(part2_name)

        if part1 and part2:
            # Detach from previous connections
            if part1.attached_to:
                part1.attached_to.attached_parts.remove(part1)
            if part2.attached_to:
                part2.attached_to.attached_parts.remove(part2)

            # Attach part2 to part1
            part2.attached_to = part1
            part1.attached_parts.append(part2)

    def detach_part(self, part_name: str):
        """Detach a part from whatever it's attached to"""
        part = self.parts.get(part_name)
        if part and part.attached_to:
            attached_to = part.attached_to
            attached_to.attached_parts.remove(part)
            part.attached_to = None


class Camera:
    """
    Simple camera class to handle viewing in 3D space
    """

    def __init__(self):
        self.position = np.array([0, 0, 10])
        self.rotation = np.array([0, 0, 0])  # Angles in radians
        self.zoom = 1.0

    def move(self, delta: np.ndarray):
        """Move the camera"""
        self.position += delta

    def rotate(self, delta: np.ndarray):
        """Rotate the camera"""
        self.rotation += delta

    def zoom_in(self, factor: float = 1.1):
        """Zoom the camera in"""
        self.zoom /= factor

    def zoom_out(self, factor: float = 1.1):
        """Zoom the camera out"""
        self.zoom *= factor


class VoxelRenderer:
    """
    Handles rendering of voxel models in 3D space
    """

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = None
        self.camera = Camera()

    def init_display(self):
        """Initialize the pygame display"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Voxel Gun Disassembly/Assembly Simulator")

    def project_3d_to_2d(self, point_3d: np.ndarray) -> Tuple[int, int]:
        """Project a 3D point to 2D screen coordinates"""
        # Simple perspective projection
        x, y, z = point_3d

        # Apply camera transformation
        transformed_x = x - self.camera.position[0]
        transformed_y = y - self.camera.position[1]
        transformed_z = z - self.camera.position[2]

        # Perspective projection
        if transformed_z == 0:
            transformed_z = 0.1  # Avoid division by zero

        scale_factor = self.camera.zoom * 100 / transformed_z

        screen_x = int(self.screen_width // 2 + transformed_x * scale_factor)
        screen_y = int(
            self.screen_height // 2 - transformed_y * scale_factor
        )  # Flip Y axis

        return screen_x, screen_y

    def render_voxel(
        self, pos_3d: np.ndarray, size: float, color: Tuple[int, int, int]
    ):
        """Render a single voxel at the given 3D position"""
        screen_pos = self.project_3d_to_2d(pos_3d)

        # Calculate size based on distance
        distance = np.linalg.norm(pos_3d - self.camera.position)
        voxel_size = max(2, int(size * 100 / (distance + 1)))

        # Draw the voxel as a square
        rect = pygame.Rect(
            screen_pos[0] - voxel_size // 2,
            screen_pos[1] - voxel_size // 2,
            voxel_size,
            voxel_size,
        )

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Black border

    def render_part(self, part: VoxelPart):
        """Render a single part with all its voxels"""
        size_x, size_y, size_z = part.get_size()

        for x in range(size_x):
            for y in range(size_y):
                for z in range(size_z):
                    if part.voxels[x, y, z]:  # If voxel is present
                        # Calculate world position of this voxel
                        world_pos = part.position + np.array([x, y, z])

                        # Render the voxel
                        self.render_voxel(world_pos, 5, part.color)

    def render_model(self, model: GunModel):
        """Render the entire gun model"""
        self.screen.fill((50, 50, 50))  # Dark gray background

        # Render all parts
        for part in model.get_all_parts():
            self.render_part(part)

        # Highlight selected part
        selected_part = model.get_selected_part()
        if selected_part:
            # Render outline around selected part
            size_x, size_y, size_z = selected_part.get_size()

            for x in range(size_x):
                for y in range(size_y):
                    for z in range(size_z):
                        if selected_part.voxels[x, y, z]:  # If voxel is present
                            # Calculate world position of this voxel
                            world_pos = selected_part.position + np.array([x, y, z])

                            # Render highlighted voxel
                            screen_pos = self.project_3d_to_2d(world_pos)
                            distance = np.linalg.norm(world_pos - self.camera.position)
                            voxel_size = max(
                                2, int(7 * 100 / (distance + 1))
                            )  # Slightly larger for highlight

                            rect = pygame.Rect(
                                screen_pos[0] - voxel_size // 2,
                                screen_pos[1] - voxel_size // 2,
                                voxel_size,
                                voxel_size,
                            )

                            pygame.draw.rect(
                                self.screen, (255, 255, 0), rect, 2
                            )  # Yellow highlight

    def handle_input(self, keys, model: GunModel):
        """Handle camera and model manipulation based on input"""
        move_speed = 0.5
        rotate_speed = 0.05

        # Camera movement
        if keys[pygame.K_w]:
            self.camera.move(np.array([0, 0, -move_speed]))
        if keys[pygame.K_s]:
            self.camera.move(np.array([0, 0, move_speed]))
        if keys[pygame.K_a]:
            self.camera.move(np.array([-move_speed, 0, 0]))
        if keys[pygame.K_d]:
            self.camera.move(np.array([move_speed, 0, 0]))
        if keys[pygame.K_q]:
            self.camera.move(np.array([0, -move_speed, 0]))
        if keys[pygame.K_e]:
            self.camera.move(np.array([0, move_speed, 0]))

        # Camera rotation
        if keys[pygame.K_UP]:
            self.camera.rotate(np.array([-rotate_speed, 0, 0]))
        if keys[pygame.K_DOWN]:
            self.camera.rotate(np.array([rotate_speed, 0, 0]))
        if keys[pygame.K_LEFT]:
            self.camera.rotate(np.array([0, -rotate_speed, 0]))
        if keys[pygame.K_RIGHT]:
            self.camera.rotate(np.array([0, rotate_speed, 0]))

        # Zoom
        if keys[pygame.K_PAGEUP]:
            self.camera.zoom_in()
        if keys[pygame.K_PAGEDOWN]:
            self.camera.zoom_out()

        # Part manipulation
        selected_part = model.get_selected_part()
        if selected_part:
            if keys[pygame.K_i]:
                selected_part.move(np.array([0, 0, -move_speed]))  # Move forward
            if keys[pygame.K_k]:
                selected_part.move(np.array([0, 0, move_speed]))  # Move backward
            if keys[pygame.K_j]:
                selected_part.move(np.array([-move_speed, 0, 0]))  # Move left
            if keys[pygame.K_l]:
                selected_part.move(np.array([move_speed, 0, 0]))  # Move right
            if keys[pygame.K_u]:
                selected_part.move(np.array([0, move_speed, 0]))  # Move up
            if keys[pygame.K_o]:
                selected_part.move(np.array([0, -move_speed, 0]))  # Move down

            # Rotation
            if keys[pygame.K_t]:
                selected_part.rotate(np.array([rotate_speed, 0, 0]))  # Rotate X
            if keys[pygame.K_g]:
                selected_part.rotate(np.array([-rotate_speed, 0, 0]))  # Rotate X
            if keys[pygame.K_f]:
                selected_part.rotate(np.array([0, rotate_speed, 0]))  # Rotate Y
            if keys[pygame.K_h]:
                selected_part.rotate(np.array([0, -rotate_speed, 0]))  # Rotate Y
            if keys[pygame.K_y]:
                selected_part.rotate(np.array([0, 0, rotate_speed]))  # Rotate Z
            if keys[pygame.K_c]:
                selected_part.rotate(np.array([0, 0, -rotate_speed]))  # Rotate Z


def create_sample_pistol() -> GunModel:
    """
    Create a sample pistol with basic parts: barrel, slide, frame, magazine
    """
    model = GunModel("Sample Pistol")

    # Define part colors
    COLORS = {
        PartType.BARREL: (100, 100, 100),  # Dark gray
        PartType.SLIDE: (120, 120, 120),  # Medium gray
        PartType.FRAME: (80, 80, 80),  # Darker gray
        PartType.MAGAZINE: (50, 50, 50),  # Black
        PartType.TRIGGER: (200, 200, 200),  # Light gray
    }

    # Barrel: 6x2x2 voxels
    barrel_voxels = np.ones((6, 2, 2))
    barrel = VoxelPart(
        "Barrel", PartType.BARREL, barrel_voxels, COLORS[PartType.BARREL]
    )
    barrel.set_position(np.array([0, 0, 0]))
    model.add_part(barrel)

    # Slide: 8x4x3 voxels
    slide_voxels = np.ones((8, 4, 3))
    # Hollow out the center for the barrel
    slide_voxels[2:6, 1:3, 1:] = 0
    slide = VoxelPart("Slide", PartType.SLIDE, slide_voxels, COLORS[PartType.SLIDE])
    slide.set_position(np.array([0, 1, -1]))
    model.add_part(slide)

    # Frame: 10x6x4 voxels
    frame_voxels = np.ones((10, 6, 4))
    # Hollow out grip area
    frame_voxels[6:, 2:5, 1:3] = 0
    frame = VoxelPart("Frame", PartType.FRAME, frame_voxels, COLORS[PartType.FRAME])
    frame.set_position(np.array([0, 0, 1]))
    model.add_part(frame)

    # Magazine: 4x2x2 voxels
    mag_voxels = np.ones((4, 2, 2))
    magazine = VoxelPart(
        "Magazine", PartType.MAGAZINE, mag_voxels, COLORS[PartType.MAGAZINE]
    )
    magazine.set_position(np.array([7, 3, 2]))
    model.add_part(magazine)

    # Trigger: 2x1x1 voxels
    trigger_voxels = np.ones((2, 1, 1))
    trigger = VoxelPart(
        "Trigger", PartType.TRIGGER, trigger_voxels, COLORS[PartType.TRIGGER]
    )
    trigger.set_position(np.array([8, 3, 3]))
    model.add_part(trigger)

    # Start with the frame selected
    model.select_part("Frame")

    return model


def main():
    """Main function to run the voxel gun simulator"""
    # Initialize Pygame
    renderer = VoxelRenderer(800, 600)
    renderer.init_display()

    # Create sample pistol model
    model = create_sample_pistol()

    # Create font for instructions
    font = pygame.font.SysFont(None, 24)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle keyboard shortcuts
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    model.select_part("Barrel")
                elif event.key == pygame.K_2:
                    model.select_part("Slide")
                elif event.key == pygame.K_3:
                    model.select_part("Frame")
                elif event.key == pygame.K_4:
                    model.select_part("Magazine")
                elif event.key == pygame.K_5:
                    model.select_part("Trigger")
                elif event.key == pygame.K_SPACE:
                    # Reset camera
                    renderer.camera = Camera()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        renderer.handle_input(keys, model)

        # Render the scene
        renderer.render_model(model)

        # Draw UI text
        instructions = [
            "CONTROLS:",
            "WASDQE: Move camera",
            "Arrow Keys: Rotate camera",
            "PgUp/PgDown: Zoom",
            "IJKL: Move selected part",
            "UO: Up/Down selected part",
            "TG: Rotate X-axis",
            "FH: Rotate Y-axis",
            "YC: Rotate Z-axis",
            "1-5: Select parts",
            "Space: Reset view",
            "ESC: Quit",
        ]

        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (255, 255, 255))
            renderer.screen.blit(text_surface, (10, 10 + i * 25))

        # Show selected part
        selected = model.get_selected_part()
        if selected:
            selected_text = f"Selected: {selected.name}"
            text_surface = font.render(selected_text, True, (255, 255, 0))
            renderer.screen.blit(text_surface, (10, 300))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
