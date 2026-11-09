from enum import Enum


class Layer(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"


class Route(str, Enum):
    ROUTE_A = "ROUTE_A"
    ROUTE_B = "ROUTE_B"
    ROUTE_C = "ROUTE_C"


class FruitLevel(str, Enum):
    F0 = "F0"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"


class TreeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    PROMOTED = "PROMOTED"
    REWORK = "REWORK"
    ARCHIVED = "ARCHIVED"


class ReworkStatus(str, Enum):
    ARCHIVED_DEAD_END = "ARCHIVED_DEAD_END"
    REUSABLE = "REUSABLE"
    INVESTIGATING = "INVESTIGATING"
