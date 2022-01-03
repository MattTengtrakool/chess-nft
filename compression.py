import tinify
from configs import tinify_API


tinify.key = tinify_API
def compress_image(filename):
    try:
        source = tinify.from_file(filename)
        source.to_file(f"o{filename}")
        return f"o{filename}"
    except Exception:
        return False
