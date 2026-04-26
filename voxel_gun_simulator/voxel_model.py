"""
VoxelModel module handles the 3D voxel representation of gun parts.
Each part is represented as a 3D array of colors.
"""


class VoxelModel:
    """
    Represents a 3D voxel model as a 3D array of color values.
    Each voxel is represented by a color tuple (R, G, B) or None if empty.
    """

    def __init__(self, width, height, depth, default_color=None):
        """
        Initialize a 3D array representing the voxel model

        Args:
            width (int): Width of the voxel grid
            height (int): Height of the voxel grid
            depth (int): Depth of the voxel grid
            default_color: Default color for all voxels (None means empty)
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.voxels = [
            [[default_color for _ in range(depth)] for _ in range(height)]
            for _ in range(width)
        ]

    def set_voxel(self, x, y, z, color):
        """
        Set a voxel at position (x, y, z) to the given color

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            color: Color value (R, G, B) or None
        """
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            self.voxels[x][y][z] = color

    def get_voxel(self, x, y, z):
        """
        Get the color at position (x, y, z)

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate

        Returns:
            Color value at the position or None if empty/out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.voxels[x][y][z]
        return None

    def copy(self):
        """
        Create a copy of this voxel model

        Returns:
            VoxelModel: A copy of this model
        """
        new_model = VoxelModel(self.width, self.height, self.depth)
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    new_model.set_voxel(x, y, z, self.get_voxel(x, y, z))
        return new_model

    def translate(self, dx, dy, dz):
        """
        Translate the entire model by the given offsets

        Args:
            dx (int): X offset
            dy (int): Y offset
            dz (int): Z offset

        Returns:
            VoxelModel: New translated model
        """
        new_model = VoxelModel(self.width, self.height, self.depth)
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    color = self.get_voxel(x, y, z)
                    if color is not None:
                        new_model.set_voxel(x + dx, y + dy, z + dz, color)
        return new_model

    def rotate_x(self):
        """
        Rotate the model around the X axis

        Returns:
            VoxelModel: New rotated model
        """
        # Calculate new dimensions after rotation
        new_width = self.width
        new_height = self.depth
        new_depth = self.height

        new_model = VoxelModel(new_width, new_height, new_depth)

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    color = self.get_voxel(x, y, z)
                    if color is not None:
                        # Apply rotation transformation
                        new_y = z
                        new_z = self.height - 1 - y
                        new_model.set_voxel(x, new_y, new_z, color)

        return new_model

    def rotate_y(self):
        """
        Rotate the model around the Y axis

        Returns:
            VoxelModel: New rotated model
        """
        # Calculate new dimensions after rotation
        new_width = self.depth
        new_height = self.height
        new_depth = self.width

        new_model = VoxelModel(new_width, new_height, new_depth)

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    color = self.get_voxel(x, y, z)
                    if color is not None:
                        # Apply rotation transformation
                        new_x = z
                        new_z = self.width - 1 - x
                        new_model.set_voxel(new_x, y, new_z, color)

        return new_model

    def rotate_z(self):
        """
        Rotate the model around the Z axis

        Returns:
            VoxelModel: New rotated model
        """
        # Calculate new dimensions after rotation
        new_width = self.height
        new_height = self.width
        new_depth = self.depth

        new_model = VoxelModel(new_width, new_height, new_depth)

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    color = self.get_voxel(x, y, z)
                    if color is not None:
                        # Apply rotation transformation
                        new_x = y
                        new_y = self.width - 1 - x
                        new_model.set_voxel(new_x, new_y, z, color)

        return new_model
