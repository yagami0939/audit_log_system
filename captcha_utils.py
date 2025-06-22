from captcha.image import ImageCaptcha
import random
import string

def generate_captcha():
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    print(text)
    image = ImageCaptcha()
    image_data = image.generate(text)
    return text, image_data
