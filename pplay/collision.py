# coding= utf-8

# Modules import
import pygame
from pygame import Rect

from pplay.baseobject import BaseObject, BaseRectObject
from pplay.point import Point

# -*- coding: utf-8 -*-

"""A simple class to deal with basic collision methods"""
"""
Must note that the collision is inclusive, i.e.,
occurs when one enters the other effectively,
not only when over the same position of the edge.
"""


class Collision:
    @classmethod
    def get_perfect_rect(cls, obj: BaseRectObject) -> Rect:
        if hasattr(obj, "curr_frame"):
            return Rect(obj.curr_frame * obj.width, 0, obj.width, obj.height)
        return obj.rect

    """
    minN: the Point of the top left of the N rect
    maxN: the Point of the bottom right of the N rect
    """

    @classmethod
    def collided_rect(cls, min1, max1, min2, max2):
        if min1.x >= max2.x or max1.x <= min2.x:
            return False
        if min1.y >= max2.y or max1.y <= min2.y:
            return False
        return True

    """
    args[0]: the origin Point
    args[1]: the target Point
    """

    @classmethod
    def collided(cls, obj: BaseObject, target: BaseObject):
        obj_min = Point(obj.x, obj.y)
        obj_max = Point(obj.x + obj.width, obj.y + obj.height)

        target_min = Point(target.x, target.y)
        target_max = Point(target.x + target.width, target.y + target.height)

        return cls.collided_rect(obj_min, obj_max, target_min, target_max)

    """
    Perfect-pixel collision using masks.
    """

    @classmethod
    def perfect_collision(cls, obj: BaseRectObject, target: BaseRectObject):
        """
        Both objects must extend a BaseRectObject,
        since it has the pygame.mask and pygame.Rect
        """
        if not hasattr(obj, "rect") or not hasattr(target, "rect"):
            return False

        obj_rect = cls.get_perfect_rect(obj)
        target_rect = cls.get_perfect_rect(target)

        offset_x = target_rect.left - obj_rect.left
        offset_y = target_rect.top - obj_rect.top

        obj_image = obj.image.subsurface(obj_rect)
        target_image = target.image.subsurface(target_rect)

        mask_1 = pygame.mask.from_surface(obj_image)
        mask_2 = pygame.mask.from_surface(target_image)

        return not not mask_1.overlap(mask_2, (offset_x, offset_y))

    """
    Perfect collision aux - is called by GameImage
    """

    @classmethod
    def collided_perfect(cls, obj: BaseRectObject, target: BaseRectObject):
        return Collision.perfect_collision(obj, target)
