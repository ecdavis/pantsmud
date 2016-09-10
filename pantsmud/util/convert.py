"""
Utility methods for data conversions, etc.
"""

import base64
import uuid


def uuid_to_base32(u):
    """
    Convert a UUID to Base32. Strips the trailing padding (six '=' characters) after conversion.
    """
    return base64.b32encode(u.bytes)[:-6]


def base32_to_uuid(s):
    """
    Convert a Base32 string to a UUID. Adds trailing padding (siz '=' characters) before conversion.
    """
    return uuid.UUID(base64.b32decode(s+('='*6)))
