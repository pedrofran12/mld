# obtain TYPE_CHECKING (for type hinting)
try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
