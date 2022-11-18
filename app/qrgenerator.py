import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def qrgenerator(url, pin, id):
    # Teil mit Pin erstellen
    img = Image.new('RGB', (330, 330), color = (255, 255, 255))

    pin_img = Image.new('RGB', (300, 40), color = (255, 255, 255))
    font = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-HeavyItalic.ttf', 30)
    d = ImageDraw.Draw(pin_img)
    d.text((130,0), pin, fill=(0,0,0), font=font)

    # QR Teil erstellen
    qr = qrcode.QRCode(
        box_size=10
    )
    
    # Domain zu url hinzfügen
    domain = os.environ.get('DOMAIN') or 'http://127.0.0.1:5000'
    url = domain + url
    
    qr.add_data(url)
    qr.make
    qr_img = qr.make_image()
    qr_img = qr_img.resize((310, 310), Image.NEAREST)

    # Beide Teile verbinden
    img.paste(qr_img, (10, 0))
    img.paste(pin_img, (0, 290))

    pfad = 'app/static/temp_files/qr_{}.jpg'.format(id)
    img.save(pfad)

    return '/temp_files/qr_{}.jpg'.format(id)


#qrgenerator('test.at', '1234', '23')