from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name='书籍名称')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='价格')
    pud_status = models.IntegerField(choices=((0, '未出版'), (1, '已出版')), default=1, verbose_name='是否出版')
    pub_date = models.DateField(verbose_name='出版日期')
    publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE, verbose_name='出版社')
    authors = models.ManyToManyField(to='Author', verbose_name='作者')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '书籍'


class Publish(models.Model):
    name = models.CharField(max_length=32, verbose_name='出版社')
    addr = models.CharField(max_length=32, verbose_name='地址')
    email = models.CharField(max_length=32, verbose_name='邮件地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '出版社'


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name='名字')
    gender = models.IntegerField(default=1, choices=((1, '男'), (2, '女')), verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    auhthorDetail = models.OneToOneField(to='AuthorDetail', on_delete=models.CASCADE, verbose_name='作者详情')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作者'


class AuthorDetail(models.Model):
    birthday = models.DateField(verbose_name='生日')
    telephone = models.CharField(max_length=32, verbose_name='电话号码')
    addr = models.CharField(max_length=32, verbose_name='地址')

    def __str__(self):
        return self.telephone

    class Meta:
        verbose_name = '作者详情'