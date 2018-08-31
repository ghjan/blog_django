# _*_ coding: utf-8 _*_

from django.db import models


class Category(models.Model):
    # 可以通过第一个参数传入字符串设置别名
    name = models.CharField("分类", max_length=100)

    # 查找 Category 时，返回为一个 object 如果不重写 __str__ 方法返回数据直接显示 Category Object，
    # 重写该方法后，查找返回结果为该方法返回的值
    def __str__(self):
        return '<Category>[{}]'.format(self.name)

    # 通过 Meta 来修改数据表的信息
    class Meta:
        db_table = "category"  # 修改数据库表名，默认表名会是 项目名_模型名 blog_category
        ordering = ['-id']  # 修改排序方式，"-" 表示逆序
