import boto3
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from io import BytesIO
from PIL import Image

from utils.constant import constant_dict

s3_client = boto3.client(
    's3',
    aws_access_key_id=constant_dict.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=constant_dict.get("AWS_SECRET_ACCESS_KEY"),
    region_name=constant_dict.get("AWS_REGION")
)


def generate_unique_filename(original_filename):
    """
    Generate a unique filename to prevent collisions

    Args:
        original_filename: Original filename from upload

    Returns:
        str: Unique filename with timestamp and UUID
    """
    # Get file extension
    file_parts = original_filename.rsplit('.', 1)
    extension = file_parts[1] if len(file_parts) > 1 else ''

    # Generate unique filename with timestamp and UUID
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]

    if extension:
        return f"{timestamp}_{unique_id}.{extension}"
    return f"{timestamp}_{unique_id}"

def get_content_type(filename):
    """
    Determine content type based on file extension

    Args:
        filename: Name of the file

    Returns:
        str: MIME type for the file
    """
    extension = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''

    # Common content types
    content_types = {
        # Images
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'svg': 'image/svg+xml',
        'bmp': 'image/bmp',
        'ico': 'image/x-icon',

        # Videos
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
        'flv': 'video/x-flv',
        'webm': 'video/webm',
        'mkv': 'video/x-matroska',

        # Audio
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'aac': 'audio/aac',
        'm4a': 'audio/mp4',

        # Documents
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'txt': 'text/plain',
        'csv': 'text/csv',

        # Archives
        'zip': 'application/zip',
        'rar': 'application/x-rar-compressed',
        '7z': 'application/x-7z-compressed',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',

        # Other
        'json': 'application/json',
        'xml': 'application/xml',
        'html': 'text/html',
        'css': 'text/css',
        'js': 'application/javascript',
    }

    return content_types.get(extension, 'application/octet-stream')

def upload_file(
        file,
        folder="",
        user_id="",
        max_file_size=50*1024*1024
):
    """
    Upload a file to S3 and return the public URL

    Args:
        file: File object
        folder: Optional subfolder within the upload folder
        user_id: Optional user ID to organize files by user
    """
    try:
        region_name = constant_dict.get("AWS_REGION")
        bucket_name = constant_dict.get("S3_BUCKET_NAME")
        upload_folder = constant_dict.get("S3_UPLOAD_FOLDER")

        # Read file content
        file.seek(0)
        file_content = file.read()
        file_size = len(file_content)

        # Check file size
        if file_size > max_file_size:
            max_size_mb = max_file_size / (1024 * 1024)
            return False, f"File size exceeds maximum allowed size of {max_size_mb}MB", None

        if file_size == 0:
            return False, "File is empty", None

        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename or "file")

        # Construct S3 object key
        key_parts = [upload_folder]
        if user_id:
            key_parts.append(f"user_{user_id}")
        if folder:
            key_parts.append(folder)
        key_parts.append(unique_filename)

        object_key = '/'.join(key_parts)

        # Determine content type
        content_type = get_content_type(unique_filename)

        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=file_content,
            ContentType=content_type,
            # Add metadata
            Metadata={
                'original-filename': unique_filename,
                'upload-timestamp': datetime.utcnow().isoformat()
            }
        )

        # Construct public URL
        public_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_key}"

        return True, "File uploaded successfully", public_url

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        return False, f"AWS S3 Error ({error_code}): {error_message}", None

    except Exception as e:
        return False, f"Upload failed: {str(e)}", None

    finally:
        # Reset file pointer for potential reuse
        file.seek(0)


def upload_image_to_s3(
        image_data,
        filename,
        folder="",
        user_id="",
        content_type="image/png"
):
    """
    Upload image data (PIL Image or bytes) to S3 and return the public URL

    Args:
        image_data: PIL Image object or bytes data
        filename: Desired filename (will be made unique)
        folder: Optional subfolder within the upload folder
        user_id: Optional user ID to organize files by user
        content_type: MIME type of the image (default: image/png)

    Returns:
        tuple: (success: bool, message: str, url: str or None)
    """
    try:
        region_name = constant_dict.get("AWS_REGION")
        bucket_name = constant_dict.get("S3_BUCKET_NAME")
        upload_folder = constant_dict.get("S3_UPLOAD_FOLDER")

        # Convert PIL Image to bytes if necessary
        if isinstance(image_data, Image.Image):
            buffer = BytesIO()
            # Determine format from filename or default to PNG
            image_format = filename.split('.')[-1].upper()
            if image_format.lower() in ['jpg', 'jpeg']:
                image_format = 'JPEG'
            elif image_format.lower() not in ['png', 'gif', 'bmp', 'webp']:
                image_format = 'PNG'

            image_data.save(buffer, format=image_format)
            file_content = buffer.getvalue()
        elif isinstance(image_data, bytes):
            file_content = image_data
        else:
            return False, "Invalid image data type. Must be PIL Image or bytes", None

        file_size = len(file_content)

        # Check file size (30MB limit)
        max_file_size = 30 * 1024 * 1024
        if file_size > max_file_size:
            max_size_mb = max_file_size / (1024 * 1024)
            return False, f"File size exceeds maximum allowed size of {max_size_mb}MB", None

        if file_size == 0:
            return False, "File is empty", None

        # Generate unique filename
        unique_filename = generate_unique_filename(filename)

        # Construct S3 object key
        key_parts = [upload_folder]
        if user_id:
            key_parts.append(f"user_{user_id}")
        if folder:
            key_parts.append(folder)
        key_parts.append(unique_filename)

        object_key = '/'.join(key_parts)

        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=file_content,
            ContentType=content_type,
            Metadata={
                'original-filename': filename,
                'upload-timestamp': datetime.utcnow().isoformat()
            }
        )

        # Construct public URL
        public_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_key}"

        return True, "Image uploaded successfully", public_url

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        return False, f"AWS S3 Error ({error_code}): {error_message}", None

    except Exception as e:
        return False, f"Upload failed: {str(e)}", None
