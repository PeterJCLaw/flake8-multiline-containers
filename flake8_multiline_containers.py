import enum

import attr


class ErrorCode(enum.Enum):
    JS101 = "Multi-line container not broken after opening character"
    JS102 = "Multi-line container does not close on same column as opening"


def _error(line_number: int, column: int, error_code: ErrorCode) -> tuple:
    """Format error report such that it's usable by flake8's reporting."""
    return (line_number, column, f'{error_code.name} {error_code.value}', None)


@attr.s(hash=False)
class MultilineContainers:
    """Ensure the consistency of multiline dict and list style."""

    name = 'flake8_multiline_containers'
    version = '0.0.15'

    errors = attr.ib(factory=list)

    def __iter__(self):
        """Entry point for the plugin."""

        return iter(self.errors)
