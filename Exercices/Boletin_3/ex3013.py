class Vector4D():
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, vector):
        return Vector4D(
            self.x + vector.x,
            self.y + vector.y,
            self.z + vector.z,
            self.w + vector.w
        )

    def __sub__(self, vector):
        return Vector4D(
            self.x - vector.x,
            self.y - vector.y,
            self.z - vector.z,
            self.w - vector.w
        )

    def __mul__(self, vector):
        return Vector4D(
            self.x * vector.x,
            self.y * vector.y,
            self.z * vector.z,
            self.w * vector.w
        )

    def __truediv__(self, escalar):
        return Vector4D(
            self.x / escalar,
            self.y / escalar,
            self.z / escalar,
            self.w / escalar
        )

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

if __name__ == "__main__":
    v1 = Vector4D(1, 2, 3, 4)
    v2 = Vector4D(5, 6, 7, 8)

    print("Vector 1:", v1)
    print("Vector 2:", v2)
    print("Suma:", v1 + v2)
    print("Resta:", v1 - v2)
    print("Multiplicación:", v1 * v2)
    print("División escalar:", v2 / 2)