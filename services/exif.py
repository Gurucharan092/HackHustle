# from PIL import Image
#
# def check_exif(image_path):
#     img = Image.open(image_path)
#
#     exif = img.getexif()
#
#     return "OK"
from PIL import Image, ExifTags
from datetime import datetime

def check_exif(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return "MISSING"

        exif = {
            ExifTags.TAGS.get(tag, tag): value
            for tag, value in exif_data.items()
        }

        date_str = exif.get("DateTimeOriginal") or exif.get("DateTime")

        if not date_str:
            return "MISSING"

        image_time = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

        if (datetime.now() - image_time).days > 30:
            return "OLD"

        return "VALID"

    except:
        return "ERROR"