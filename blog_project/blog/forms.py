# _*_ coding: utf-8 _*_

from django import forms
from .models import Post


# 表单类必须继承 forms.ModelForm 或者 forms.Form 类，如果有相应的模型，则使用 ModelForm 更方便
class PostForm(forms.ModelForm):
    class Meta:
        # 表单对应的数据库模型
        model = Post
        # 指定表单需要显示的字段
        fields = ['title', 'body']


# 假设有个信息反馈的表单
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'clos': 80, 'rows': 20}))

    # 自定义校验规则，以 clean 开头，字段名结尾，校验时候自动调用方法
    # 例如过滤信息长度小于 4 个字的信息，提示用户修改
    def clean_message(self):
        self.message = message = self.cleaned_data['message']
        num_word = len(message.split())
        if num_word < 4:
            raise forms.ValidationError('Not Enough words')
        return message
