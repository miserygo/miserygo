from django.db import models

# 用户表
class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Hot(models.Model):
    id = models.IntegerField(primary_key=True)
    title=models.CharField(max_length=100,)
    content=models.CharField(max_length=200,blank=True, null=True)
    url=models.CharField(max_length=100,)
    block_id=models.ForeignKey('Block', related_name = "hot")


class Block(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100,)
    hots=models.OneToOneField('Hot',
                              on_delete=models.CASCADE)