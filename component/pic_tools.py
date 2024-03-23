# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-03-23 19:29:26
#FilePath: \ghost_sa_github_cgq\component\pic_tools.py
#
import sys
sys.path.append('./')
# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw
import qrcode
from configs import admin
from configs.export import write_to_log
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

def gen_text_img(text,font_size=11, font =admin.font ,font_color=(0,0,0), bg_color=(255,255,255),max_width=1000,max_height=2000):
    # 检测需要的图片大小
    height = font_size
    width = font_size
    for line in text.split('\n'):
        width = max(width, len(line) * font_size) 
        height += font_size
    width = width + font_size
    if width > max_width:
        width = max_width
    if height > max_height:
        height = max_height
    # 创建一个空白图像
    image = Image.new('RGB', (width, int(height*1.5)), bg_color)
    try:
        font = ImageFont.truetype(font,font_size)
        draw = ImageDraw.Draw(image)
        # 绘制文本
        draw.text((0, 0), text, font=font, fill=font_color)
        output_buffer = BytesIO()
        image.save(output_buffer, format='GIF')
        return output_buffer.getvalue()
    except:
        write_to_log(filename='pic_tools.py',defname='gen_text_img',result='字体文件不存在')
        bitimage1 = os.path.join('image','43byte.gif')
        with open(bitimage1, 'rb') as f:
            returnimage = f.read()
        return returnimage