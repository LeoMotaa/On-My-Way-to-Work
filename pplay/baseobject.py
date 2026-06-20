"""Base Object Module

Contains the most basics objects. BaseObject, an object that contains the
position and size of the Object and the BaseRectObject, an object that
contains the `rect` and `image` of the Object.
"""

from typing import Optional

from pygame.rect import Rect
from pygame.surface import Surface


class BaseObject:
    """Handle the coords and size of an Object.

    Attributes:
        x: An integer indicating the x coord.
        y: An integer indicating the y coord.
        width: An integer indicating width of object.
        height: An integer indicating height of object.
    """

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.width: int = 0
        self.height: int = 0


class BaseRectObject(BaseObject):
    """Handle the `rect` and `image` of an Object.

    Attributes:
        rect: An `Rect` of the Object.
        image: An `Surface` of the Object.
    """

    def __init__(self):
        super(BaseRectObject, self).__init__()
        self.rect: Optional[Rect] = None
        self.image: Optional[Surface] = None
