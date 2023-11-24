"""
- __init__() -  инициализация экземпляра класса. Конструирует новый объект типа Vector3D 
                из трех чисел с плавающей точкой(float). По умолчанию конструирует нулевой вектор. 
                Если пользователь попытается инициализировать объект нечисловыми типами, 
                необходимо бросить исключение;  
- __repr__() -  возвращает текстовую строку: `'Vector3D(x, y, z)'`, где x, y, z - значения компонент;  
- __abs__() -   возвращает длину вектора;  
- __bool__() -  возвращает True, если вектор ненулевой, иначе - False;  
- __eq__(other) - сравнивает два вектора, возвращает True, если векторы равны покомпонентно, иначе False;  
- __neg__() -   возвращает новый объект типа Vector3D, компоненты которого равны компонентам данного вектора, 
                домноженным на минус единицу;  
- __add__(other) - складывает два вектора, возвращает новый объект типа Vector3D - сумму;  
- __sub__(other) - вычитает вектор other из данного вектора, возвращает новый объект типа Vector3D - разность;  
- __mul__(scalar) - умножение вектора на скаляр слева, возвращает новый объект типа Vector3D - произведение;  
- __rmul__(scalar) - умножение вектора на скаляр справа, возвращает новый объект типа Vector3D - произведение;  
- __truediv__(scalar) - деление вектора на скаляр, возвращает новый объект типа Vector3D - частное;  
- dot(other) - возвращает результат скалярного произведения;  
- cross(other) - возвращает векторное произведение между векторами; 

"""
from typing import Generator, Any

class Vector3D:
    _x: float
    _y: float
    _z: float
    
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float =0
    ) -> None:
        if (isinstance(x, int) or isinstance(x, float)) and \
                (isinstance(y, int) or isinstance(y, float)) and \
                (isinstance(z, int) or isinstance(z, float)):
            self._x = x
            self._y = y
            self._z = z
        else:
            raise ValueError("coords must be numbers")
        
    def __iter__(self) -> Generator[float, float, float]:
        coords = (self._x, self._y, self._z)

        return (coord for coord in coords)
    
    def __repr__(self) -> str:
        return f"Vector3D({self._x}, {self._y}, {self._z})"
    
    def __abs__(self) -> float:
        x = self._x
        y = self._y
        z = self._z
        return (x**2 + y**2 +z**2)**0.5
    
    def __bool__(self) -> bool:
        if self.__abs__ == 0:
            return False
        return True
    
    def __eq__(self, other: Any) -> bool:    
        x1 = self._x
        y1 = self._y
        z1 = self._z

        x2 = other._x
        y2 = other._y
        z2 = other._z

        if (x1 == x2) and (y1 == y2) and (z1 == z2):
            return True
        return False 
    
    def __neg__(self):
        return Vector3D(-self._x, -self._y, -self._z)
    
    def __add__(self, other):
        x1 = self._x
        y1 = self._y
        z1 = self._z

        x2 = other._x
        y2 = other._y
        z2 = other._z

        return Vector3D(x1+x2, y1+y2, z1+z2)
    
    def __sub__(self, other):
        # x1 = self._x
        # y1 = self._y
        # z1 = self._z

        # x2 = other._x
        # y2 = other._y
        # z2 = other._z

        # return Vector3D(x1-x2, y1-y2, z1-z2)

        return self + (-other)
    
    def __mul__(self, scalar: float):
        return Vector3D(scalar * self._x, scalar * self._y, scalar * self._z)

    def __rmul__(self, scalar: float):
        # return Vector3D(scalar * self._x, scalar * self._y, scalar * self._z)
        return scalar * self
    
    def __truediv__(self, scalar):
        # return Vector3D(self._x / scalar, self._y/scalar, self._z/scalar)
        return self * (1/scalar)

    
    def dot(self, other) -> float:
        x1 = self._x
        y1 = self._y
        z1 = self._z

        x2 = other._x
        y2 = other._y
        z2 = other._z

        return x1*x2+y1*y2+z1*z2
    
    def cross(self, other):
        x1 = self._x
        y1 = self._y
        z1 = self._z

        x2 = other._x
        y2 = other._y
        z2 = other._z

        new_x = (y1*z2 - y2*z1)
        new_y = -(x1*z2 - x2*z1)
        new_z = (x1*y2 - x2*y1)

        return Vector3D(new_x, new_y, new_z)
    
    def cos_between_vecs(self, other):
        dot_mult = self.dot(other)
        abs1 = abs(self)
        abs2 = abs(other)

        cos = dot_mult/(abs1*abs2)

        return cos
    def sin_between_vecs(self, other):
        cross_mult = self.cross(other)
        abs1 = abs(self)
        abs2 = abs(other)

        cos = abs(cross_mult)/(abs1*abs2)

        return cos
    def sin_between_vecs(self, other):
        cross_mult = self.cross(other)
        abs1 = abs(self)
        abs2 = abs(other)

        cos = abs(cross_mult)/(abs1*abs2)

        return cos
# Если бы сделали приватными атрибуты
    @property
    def x(self) -> float:
        return self.x
    
    @property
    def y(self) -> float:
        return self.y
    
    @property
    def z(self) -> float:
        return self.z

v1 = Vector3D(1,2,3)
v2 = Vector3D(1,2,3)

print(v1.__repr__)
print(v1)

print(v1.cross(v2))

print(v1.cos_between_vecs(v2))
print(v1.sin_between_vecs(v2))

nachalo = Vector3D(1,2,3)
konec = Vector3D(2,7,6)

point = (0,3,6)

def rasst_ot_otrezka_do_tochki(nachalo, konec, point):
    pass
