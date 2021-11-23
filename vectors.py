import math
import numpy as np

from abc import ABC, abstractmethod

class IPolar2D(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_angle(self):
        pass

    @abstractmethod
    def abs(self):
        pass


class IVector(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def abs(self):
        pass

    @abstractmethod
    def c_dot(self):
        pass

    @abstractmethod
    def get_components(self):
        pass


class Vector2D(IVector):

    def __init__(self,x,y):

        self._x = x
        self._y = y

    def get_components(self):
        return [self._x,self._y]

    def abs(self):
        return math.sqrt(self._x ** 2 + self._y ** 2)

    def c_dot(self, vec: IVector):
        return self._x * vec.get_components()[0] + self._y * vec.get_components()[1]

class Polar2DAdapter(IVector, IPolar2D):

    def __init__(self, srcVector: Vector2D):
        self._srcVector = srcVector

    def abs(self):
        return math.sqrt(self._srcVector.get_components()[0] ** 2 + self._srcVector.get_components()[1] ** 2)

    def get_angle(self):
        return math.atan2(self._y, self._x) * 180 / math.pi

    def c_dot(self, vec: IVector):
        return self._srcVector.get_components()[0] * vec.get_components()[0] + self._srcVector.get_components()[1] * vec.get_components()[1]

    def get_components(self):
        pass


class Vector3DDecorator(IVector):

    def __init__(self, vec:IVector, z):
        self._src_vector = vec
        self._z = z

    def abs(self):
        return math.sqrt(self._src_vector.get_components()[0]**2+self._src_vector.get_components()[1]**2+self._z**2)

    def c_dot(self, vec: IVector):
        return self._src_vector.get_components()[0] * vec.get_components()[0] + self._src_vector.get_components()[1] * vec.get_components()[1] + self._z**2

    def get_components(self):
        return [self._src_vector.get_components()[0], self._src_vector.get_components()[1], self._z]

    def cross(self, vec: IVector):
        return np.cross(self.get_components(), vec.get_components())

    def get_src_v(self):
        return self._src_vector


class TwoDPolarInheritance(Vector2D):

    def __init__(self,x,y):
        super().__init__(x,y)

    def get_angle(self):
        return math.atan2(self._y, self._x) * 180 / math.pi

class VectorThreeDInheritance(Vector2D):

    def __init__(self,x,y,z):
        super().__init__(x,y)
        self._z = z

    def abs(self):
        return math.sqrt(self.__z**2+self._y**2+self._x**2)

    def c_dot(self, vec: IVector):
        return self._x * vec.get_components()[0] + self._y * vec.get_components()[1] + self._z * vec.get_components()[2]

    def get_components(self):
        return [self._x, self._y, self._z]

    def cross(self, vec: IVector):
        return np.cross(self.get_components(), vec.get_components())

    def get_src_v(self):
        return Vector2D(self._x,self._y)