# core/utils/image_optimizer.py

from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from django.apps import apps
from django.db.models import ImageField, FileField


def super_optimize_image(image, max_width, max_height, target_size_kb):
    
    prefix_name = "min_"
    
    # Get original file size (bytes → MB).
    actual_size_mb = round(image.size / (1024 * 1024),3)

    # Open the uploaded image using Pillow.
    # `image` here is usually an UploadedFile or InMemoryUploadedFile object from Django.
    img = Image.open(image)

    # Fix orientation problems caused by mobile phones.
    # Many mobile cameras store rotation information in EXIF metadata instead of
    # actually rotating the pixels. This function reads that EXIF tag and rotates
    # the image correctly.
    img = ImageOps.exif_transpose(img)

    # Some formats like PNG may contain transparency (RGBA) or palette mode (P).
    # JPEG does not support transparency, so we convert such images to RGB.
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize large images while keeping aspect ratio.
    # `thumbnail()` modifies the image in place and ensures the image
    # fits inside the given dimensions without stretching.
    # Example: 4000x3000 → 1600x1200
    img.thumbnail((max_width, max_height))

    # Start compression quality.
    # JPEG quality ranges from 1–95 (Pillow recommended max).
    # Higher = better quality but larger size.
    quality = 90

    # Try compressing repeatedly until the file size becomes <= TARGET_SIZE_KB
    # or until quality drops to 30.
    size_kb = "__"

    while quality > 30:

        # Create an in-memory binary buffer.
        # Instead of saving to disk, we store the compressed image in RAM.
        buffer = BytesIO()

        # Extract EXIF metadata from original image (if available)
        exif = img.info.get("exif")

        # Save the image into the buffer as JPEG.
        img.save(
            buffer,
            format="JPEG",       # Convert all images to JPEG
            quality=quality,     # Compression quality
            optimize=True,       # Enables additional compression optimizations
            progressive=True,     # Progressive JPEG loads faster in browsers
            exif=exif            # preserve metadata
        )

        # Check the size of the compressed image in KB
        size_kb = buffer.tell() / 1024      
        
        # If the file size is below our target size, stop compressing
        if size_kb <= target_size_kb:
            break

        # Otherwise reduce quality and try again
        quality -= 5

    print(f"Compression successful at quality {quality} with size {size_kb:.2f} KB (Original: {actual_size_mb} MB)")
    # generate new file name with original size in MB and compressed size in MB and compression percentage
    # compressed_size_mb = round(size_kb / 1024,3)
    # compression_percentage = round((actual_size_mb - compressed_size_mb) / actual_size_mb * 100, 2)
    # prefix_name = f"min_{actual_size_mb}MB_{compressed_size_mb}MB_{compression_percentage}pct_{quality}q_"

    # Move the buffer cursor back to the start so Django can read the file
    buffer.seek(0)

    # Return a Django-compatible uploaded file object.
    # Django expects file uploads in this format when saving to ImageField.
    return InMemoryUploadedFile(
        buffer,                 # The compressed image data in memory
        "ImageField",           # Field name (not critical here)
        prefix_name+image.name, # New file name (prefixed with 'min_')
        "image/jpeg",           # MIME type
        buffer.tell(),          # Final file size in bytes
        None,                   # Charset (not needed for images)
    )

# Next enhancements could include:
# Advanced Django image pipeline used in large production apps that:
# compresses 20MB → ~120KB
# converts images to WebP automatically
# works with S3 + CloudFront
# supports bulk uploads + DRF APIs
# runs 2–3× faster than your current loop.



def reprocess_images(model_path: str, field_name: str, chunk_size: int = 200):
    from django.db import transaction

    try:
        app_label, model_name = model_path.split(".")
    except ValueError:
        raise ValueError("Model must be in format: app_label.ModelName")

    # Get model
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise ValueError(f"Model {model_path} not found")

    # Check field exists
    try:
        field = model._meta.get_field(field_name)
    except Exception:
        raise ValueError(f"Field '{field_name}' not found in {model_path}")

    # Allow both FileField and ImageField
    if not isinstance(field, (ImageField, FileField)):
        raise ValueError(f"Field '{field_name}' is not a FileField/ImageField")

    print(f"\nProcessing {model_path}.{field_name}\n")

    queryset = model.objects.exclude(**{field_name: ""})

    for obj in queryset.iterator(chunk_size=chunk_size):

        file_field = getattr(obj, field_name)

        if not file_field:
            continue

        try:

            print(f"Processing: {file_field.name}")

            try:
                size = file_field.size
            except FileNotFoundError:
                print(f"Missing file, skipping: {file_field.name}")
                continue

            # Skip already optimized files
            if file_field.name.startswith("min_"):
                continue

            # Skip already small files
            if size < 1024 * 1024:
                continue

            file_field.open()

            try:
                img = Image.open(file_field)
                img.load()  # faster than verify()
            except Exception:
                print(f"Skipping non-image: {file_field.name}")
                file_field.close()
                continue

            # Reset pointer
            file_field.file.seek(0)

            old_name = file_field.name

            # Save optimized version
            with transaction.atomic():
                setattr(obj, field_name, file_field.file)
                obj.save(update_fields=[field_name])

            new_name = getattr(obj, field_name).name

            print(f"Optimized → {new_name}")

            # Close before deleting (important for Windows)
            file_field.close()

            if old_name and old_name != new_name:
                try:
                    getattr(obj, field_name).storage.delete(old_name)
                    print(f"Deleted old file: {old_name}")
                except Exception as delete_error:
                    print(f"Could not delete old file {old_name}: {delete_error}")

        except Exception as e:
            print(f"Error processing {file_field.name}: {e}")