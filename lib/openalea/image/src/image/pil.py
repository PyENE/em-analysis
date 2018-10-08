
__all__ = ['Image', 'ImageQt', 'ImageOps']

try:
    import Image, ImageQt, ImageOps
except ImportError:
    try:
        from PIL import Image, ImageQt, ImageOps
    except ImportError:
        raise ImportError, "PIL not found. Please install PIL or pillow"

