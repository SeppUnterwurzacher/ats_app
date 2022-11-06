import qrcode
from PIL import Image, ImageDraw, ImageFont

def qrgenerator(url, pin):
    # Teil mit Pin erstellen
    img = Image.new('RGB', (300, 300), color = (255, 255, 255))

    pin_img = Image.new('RGB', (300, 40), color = (255, 255, 255))
    font = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-HeavyItalic.ttf', 30)
    d = ImageDraw.Draw(pin_img)
    d.text((110,0), pin, fill=(0,0,0), font=font)

    # QR Teil erstellen
    qr = qrcode.QRCode(
        box_size=10
    )
    
    qr.add_data(url)
    qr.make

    qr_img = qr.make_image()

    img.paste(qr_img)
    img.paste(pin_img, (0,255))
    # Saving as an image file

    img.save('MyQRCode1.jpg')


#qrgenerator('test.at', '1234')