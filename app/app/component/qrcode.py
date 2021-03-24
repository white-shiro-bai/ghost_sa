# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import base64
from io import BytesIO
from PIL import Image
import qrcode
import os

def gen_qrcode(args):
    qrcode_data = args['qrdata']
    logo_path = args['logo'] if 'logo' in args else None
    qr = qrcode.QRCode(border=1,error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(qrcode_data)
    img = qr.make_image().convert('RGBA')
    img_w, img_h = img.size
    factor = 4
    size_w, size_h = int(img_w / factor), int(img_h / factor)
    if logo_path and logo_path != '':
        try:
            icon = Image.open(logo_path).convert("RGBA")
            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
            w, h = int((img_w - icon_w) / 2), int((img_h - icon_h) / 2)
            img.paste(icon, (w, h), icon)
        except:
            pass
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    return output_buffer.getvalue()
