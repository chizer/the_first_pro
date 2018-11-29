from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),label=False,
                           error_messages={'required':'评论内容不能为空'})

    #在实例化时，可以接受参数，同时初始化方法需要使用父类的初始化方法
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):
        #判断用户是否登录
        if self.user.is_authenticated:
            #如果登录，则将该用户写入
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        #评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            #验证成功，则写入content_object到form表单中
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist as e:
            raise forms.ValidationError("评论对象不存在")

        return self.cleaned_data