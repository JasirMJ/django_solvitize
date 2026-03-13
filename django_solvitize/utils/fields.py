# core/fields.py

from django.db.models import ImageField

from django_solvitize.utils.utils_image_optimiser import super_optimize_image


DEFAULT_MAX_WIDTH = 1600
DEFAULT_MAX_HEIGHT = 1600
DEFAULT_TARGET_SIZE_KB = 1000

class OptimizedImageField(ImageField):
    

    def __init__(self, *args, **kwargs):
        self.COMPRESS_MAX_WIDTH = kwargs.pop('COMPRESS_MAX_WIDTH', DEFAULT_MAX_WIDTH)
        self.COMPRESS_MAX_HEIGHT = kwargs.pop('COMPRESS_MAX_HEIGHT', DEFAULT_MAX_HEIGHT)
        self.COMPRESS_TARGET_SIZE_KB = kwargs.pop('COMPRESS_TARGET_SIZE_KB', DEFAULT_TARGET_SIZE_KB)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):

        file = getattr(model_instance, self.attname)

        if file and not getattr(file, "_optimized", False):
            optimized = super_optimize_image(
                file,
                max_width=self.COMPRESS_MAX_WIDTH,
                max_height=self.COMPRESS_MAX_HEIGHT,
                target_size_kb=self.COMPRESS_TARGET_SIZE_KB
            )
            optimized._optimized = True

            print("Original size:", file.size / 1024 / 1024, "MB")
            print("Optimized size:", optimized.size / 1024, "KB")
            setattr(model_instance, self.attname, optimized)

        return super().pre_save(model_instance, add)