"""
Image resources for the To-Do application.
This module manages the resource paths and loads images for the UI.
"""
import os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/images")
os.makedirs(IMAGE_DIR, exist_ok=True)
DEFAULT_BANNER = os.path.join(IMAGE_DIR, "banner.png")
DEFAULT_LOGO = os.path.join(IMAGE_DIR, "logo.png")
DEFAULT_AVATAR = os.path.join(IMAGE_DIR, "avatar.png")
LOGIN_BANNER = os.path.join(IMAGE_DIR, "login_banner.png")
REGISTER_BANNER = os.path.join(IMAGE_DIR, "register_banner.png")
TASK_BANNER = os.path.join(IMAGE_DIR, "task_banner.png")

def get_pixmap(path, default=None):
    """
    Load an image as a QPixmap, with fallback to default if the file doesn't exist.
    
    Args:
        path: Path to the image file
        default: Default image path to use if the file doesn't exist
        
    Returns:
        QPixmap: The loaded image
    """
    if os.path.exists(path):
        return QPixmap(path)
    elif default and os.path.exists(default):
        return QPixmap(default)
    else:
        return QPixmap()

def get_icon(path, default=None, size=None):
    """
    Load an image as a QIcon, with fallback to default if the file doesn't exist.
    
    Args:
        path: Path to the image file
        default: Default image path to use if the file doesn't exist
        size: Optional QSize to set the icon size
        
    Returns:
        QIcon: The loaded icon
    """
    pixmap = get_pixmap(path, default)
    
    if size and not pixmap.isNull():
        pixmap = pixmap.scaled(size)
        
    return QIcon(pixmap)

def get_banner_pixmap(banner_type="default"):
    """
    Get the appropriate banner image based on the type.
    
    Args:
        banner_type: Type of banner ('default', 'login', 'register', 'task')
        
    Returns:
        QPixmap: The banner image
    """
    banner_paths = {
        "default": DEFAULT_BANNER,
        "login": LOGIN_BANNER,
        "register": REGISTER_BANNER,
        "task": TASK_BANNER
    }
    
    path = banner_paths.get(banner_type, DEFAULT_BANNER)
    return get_pixmap(path, DEFAULT_BANNER)

def get_logo_icon(size=QSize(64, 64)):
    """
    Get the application logo as an icon.
    
    Args:
        size: Size for the icon
        
    Returns:
        QIcon: The logo icon
    """
    return get_icon(DEFAULT_LOGO, size=size)
