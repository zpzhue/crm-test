from app01 import models
from stark.services.sites import site,ModelStark


class AuthorDetailConfig(ModelStark):
    list_display = ['birthday', 'telephone', 'addr']

site.register(models.Book)
site.register(models.Publish)
site.register(models.AuthorDetail, AuthorDetailConfig)
site.register(models.Author)


