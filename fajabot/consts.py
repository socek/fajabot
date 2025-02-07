from enum import Enum


class State(Enum):
    BEFORE_START = "before_start"
    RUNNING = "running"
    RESTART = "restart"
    EXITING = "exiting"
