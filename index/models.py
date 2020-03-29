from django.db import models

# Create your models here.

class im(models.Model):

    class Meta:
        permissions = (

            ("dashboard", "首页仪表盘"),
        )

