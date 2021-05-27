from django.db import models
from  django.utils import timezone
# Create your models here.

class User(models.Model):
    """用户表"""
    GENDER_CHOICE = (
        ('name','男'),  #第一项会存储到数据库中
        ('female', '女'),
        ('unknown', '未知'),
    )
    # id自增主键id，自动创建
    name = models.CharField('姓名', max_length=20)
    password = models.CharField('密码', max_length=20)
    hash_password =  models.CharField('哈希密码', max_length=128)
    gender = models.CharField('性别', choices=GENDER_CHOICE, max_length=10, default=GENDER_CHOICE[2][1], blank=True)
    email = models.CharField('邮箱', max_length=100,unique=True)
    # phone =
    register_time = models.DateTimeField('注册日期', default=timezone.now)
    # last_login_time =
    # is_active =

    def __str__(self):
        # 默认<class User>,重写此方法可以在调试时看到实例的name属性
        return f'<class User>{self.name}'

    class Meta:
        # 元信息， 可以不写
        # db_table=''    # 默认生成 模块名_类名的表    login_user
        # ordering = ['id'] # group by
        verbose_name = '用户表'
