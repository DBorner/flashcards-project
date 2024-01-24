from datetime import datetime
import os
from ckeditor_uploader.fields import RichTextUploadingField


def set_file_name(instance, filename, additional_prefix=""):
    ext = filename.split(".")[-1]

    new_filename = f"{additional_prefix}{instance.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"

    return os.path.join("uploads", new_filename)


class CustomRichTextUploadingField(RichTextUploadingField):
    def generate_filename(self, instance, filename):
        file_name = set_file_name(instance, filename)
        return super().generate_filename(instance, file_name, "fishcard_")
