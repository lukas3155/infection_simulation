from __future__ import annotations

import vectors as vc
import random
from abc import ABC, abstractmethod


class Person:

    def __init__(self, x=0, y=0):

        self.state: Context = Context(Resistant())
        self.vector = vc.Vector2D(random.randint(-30, 30), random.randint(-30, 30))
        self.last_time = 0
        self.infection_time = 0
        self.rectangle = None
        self.x = x
        self.y = y
        self.color = "blue"


class Context:

    _state = None

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):

        self._state = state
        self._state.context = self

    def request1(self, p:Person):
        self._state.handle1(p)

    def request2(self, p:Person):
        self._state.handle2(p)


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle1(self, p:Person) -> None:
        pass

    @abstractmethod
    def handle2(self, p:Person) -> None:
        pass



class Resistant(State):

    def handle1(self, p:Person):
        self.context.transition_to(NoResistant())

    def handle2(self, p:Person):
        p.color = "green"
        self.context.transition_to(Healthy())


class NoResistant(State):

    def handle1(self, p:Person):
        p.color = "green"
        self.context.transition_to(Healthy())

    def handle2(self, p:Person):
        p.color = "yellow"
        self.context.transition_to(Infected())


class Healthy(State):

    def handle1(self, p:Person):
        p.color = "yellow"
        self.context.transition_to(Infected())

    def handle2(self, p:Person):
        pass


class Infected(State):

    def handle1(self, p:Person):
        p.color = "red"
        self.context.transition_to(Symptoms())

    def handle2(self, p:Person):
        self.context.transition_to(NoSymptoms())


class Symptoms(State):

    def handle1(self, p:Person):
        p.color = "blue"
        self.context.transition_to(Resistant())

    def handle2(self, p:Person):
        pass


class NoSymptoms(State):

    def handle1(self, p:Person):
        p.color = "blue"
        self.context.transition_to(Resistant())

    def handle2(self, p:Person):
        pass
