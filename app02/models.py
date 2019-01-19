from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    passwd = models.CharField(max_length=32, verbose_name='密码')
    is_root = models.IntegerField(choices=((0, '管理员'), (1, '普通用户')), default=1, verbose_name='角色')
    def __str__(self): return self.username

    class Meta:
        verbose_name = '用户'
