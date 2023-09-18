import functools
from dataclasses import dataclass


@functools.total_ordering
@dataclass(frozen=True, order=False)
class FirmwareVersion:
    major: int
    minor: int
    patch: int

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch:
                    return True
        return False
