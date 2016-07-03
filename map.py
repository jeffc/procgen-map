#!/usr/bin/python2

from PIL import Image
from noise import snoise2
from sys import argv
import numpy as np


class Level:
  water = 1
  shore = 2
  land = 3
  ice = 4


def gen_map(
    width=512,
    height=512,
    octaves=32,
    water_level=127,
    shore_size=1,
    ice_level=230,
    ):
  levels = np.zeros( (height, width, 1), dtype=np.uint8 )
  noises = np.zeros( (height, width, 1), dtype=np.uint8 )
  colors = np.zeros( (height, width, 3), dtype=np.uint8 )
  
  freq = octaves * 16.0

  for x in range(width):
    for y in range(height):
      point = snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0
      level = None

      if point < water_level:
        level = Level.water        
      elif point >= water_level and point < (water_level + shore_size):
        level = Level.shore
      elif point > ice_level:
        level = Level.ice
      else:
        level = Level.land

      levels[y,x] = level
      noises[y,x] = point


  for x in range(width):
    for y in range(height):
      level = levels[y,x]
      point = noises[y,x]
      if level == Level.water:
        colors[y,x] = [0, 0, point * 0.5]
      elif level == Level.shore:
        colors[y,x] = [0.76 * point, 0.70 * point, 0.50 * point]
      elif level == Level.land:
        colors[y,x] = [0, (point - 128.0) * 2, 0]
      elif level == Level.ice:
        colors[y,x] = [0.66 * point, 0.83 * point, 0.89 * point]

  return colors


if __name__ == '__main__':

  img = Image.fromarray(
      gen_map(
        width=1000,
        height=1000,
        water_level=150,
        octaves=16,
        )
      )
  img.show()
