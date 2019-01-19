from app01 import models
from stark.services.sites import site


site.register(models.Book)
site.register(models.Publish)
site.register(models.AuthorDetail)
site.register(models.Author)


