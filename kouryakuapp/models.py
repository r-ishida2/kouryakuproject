from django.db import models

from accounts.models import CustomUser
# Create your models here.

class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )

    def __str__ (self):
        return self.title


# Create your models here.

class KouryakuPost(models.Model):
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
        )

    content = models.TextField(
        verbose_name='本文'
        )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='voice_user'
        )

    posted_at = models.DateTimeField(
        verbose_name = '投稿日時',
        auto_now_add=True
        )

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
        )
    
    like_num = models.IntegerField(
        default=0
        )
    
    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title





#コメントモデル
class Comment(models.Model):
    user_name = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='comment_user'
        )
    
    message = models.TextField(
        '本文'
        )
    target = models.ForeignKey(
        KouryakuPost,
        on_delete=models.CASCADE,
        verbose_name='対象記事',
        related_name='comments'
        )
    
    comment_at = models.DateTimeField(
        '作成日',
        auto_now_add=True
        )

def __str__(self):
    return f"Comment by {self.user_name.username} on {self.target.title}"

class AdminUpdate(models.Model):
    info = models.TextField(
        verbose_name='アップデート情報'
    )
    info_at = models.DateTimeField(
        verbose_name='更新日',
        auto_now_add=True
    )

    def __str__(self):
        return f"更新: {self.info_at.strftime('%Y-%m-%d')}"