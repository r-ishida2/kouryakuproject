from django.forms import ModelForm
from .models import KouryakuPost,Comment,AdminUpdate

class KouryakuPostForm(ModelForm):
    class Meta:
        # モデルのクラス
        model = KouryakuPost
        # フォームで使用するモデルのフィールドを指定
        fields = ['category', 'title', 'content']

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class AdminUpdateForm(ModelForm):
    class Meta:
        model = AdminUpdate
        fields = ['info']