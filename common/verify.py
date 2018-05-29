from PIL import Image,ImageDraw,ImageFont,ImageFilter
from tk_docker import settings
import random
import string
from io import BytesIO

#字体的位置，不同版本的系统会有不同
font_path = settings.STATICFILES_DIRS[0]+'/font/Arial.ttf'
# font_path = '/Library/Fonts/Hanzipen.ttc'
#生成几位数的验证码
number = 4
#生成验证码图片的高度和宽度
size = (280,40)
#背景颜色，默认为白色
# bgcolor = (255,255,255)
bgcolor = (73,157,134)
#字体颜色，默认为蓝色
fontcolor = (0,0,255)
#干扰线颜色。默认为红色
linecolor = (255,0,0)
#是否要加入干扰线
draw_line = True
#加入干扰线条数的上下限
line_number = (1,5)

def gen_text():
    source = list(string.ascii_lowercase)
    for index in range(0,10):
       source.append(str(index))
    return ''.join(random.sample(source,number))#number是生成验证码的位数

 #用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = linecolor)

def gene_code(request):
    width,height = size #宽和高
    image = Image.new('RGBA',(width,height),bgcolor) #创建图片
    font = ImageFont.truetype(font_path,30) #验证码的字体和字体大小
    # font = ImageFont.truetype(25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image) #创建画笔
    #text = "我是中国人" #生成字符串
    text = gen_text() #生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,font= font,fill=fontcolor) #填充字符串
    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        # image = image.transform((width + 20, height +10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        f = BytesIO()
        image.save(f, "png")
        data = f.getvalue()
        request.session["verify_code_key"] = text
        return data