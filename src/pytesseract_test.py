try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('test.jpg')))