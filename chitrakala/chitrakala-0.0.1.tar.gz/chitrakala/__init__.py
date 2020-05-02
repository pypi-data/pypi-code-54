from PIL import Image, ImageDraw, ImageFont
import time
import os

class Chitrakala:
  '''
    Annotates images and creates copies.
  '''

  PREFIX = "timestamp"

  def __init__(self, filename):
    self.filename = filename

  def annotate(self):
    '''
      Annotate with creation date at bottom right corner.
    '''

    base = Image.open(self.filename)

    creation_time = base.info['Creation Time']
    raw_time = time.strptime(creation_time, '%a %d %b %Y %I:%M:%S %p %Z')
    date = time.strftime('%Y-%m-%d', raw_time)

    text = Image.new('RGBA', base.size, (255,255,255,0))
    draw = ImageDraw.Draw(text)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    end_x, end_y = base.size
    draw.text((end_x -300,end_y -60), date, font=font, fill=(255,68,68,255))

    path, out_filename = os.path.split(self.filename)
    out_filename = '{0}_{1}'.format(self.PREFIX, out_filename)
    out = Image.alpha_composite(base, text)
    out.save("{0}/{1}".format(path, out_filename))