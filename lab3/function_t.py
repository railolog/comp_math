from typing import Callable


class Function:
    def __init__(self, f: Callable, view: str):
        self.f = f
        self.view = view

    def __str__(self):
        return self.view
