# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SupermarketsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id_producto = scrapy.Field()
    precio = scrapy.Field()
    precio_oferta = scrapy.Field()
    precio_unidad = scrapy.Field()
    fecha_chequeo = scrapy.Field()
    codigo_postal = scrapy.Field()
    plataforma = scrapy.Field()
    url = scrapy.Field()
    url_imagen = scrapy.Field()
    descripcion = scrapy.Field()
    nombre = scrapy.Field()
