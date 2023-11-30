"""Custom errors for NetFuse module.

>>> Error

"""


class Error(Exception):
    """Package's base exception."""


class ValidationError(ValueError):
    """Custom validation error."""


class MissingRequirement(ImportError):
    """Custom requirement error."""
