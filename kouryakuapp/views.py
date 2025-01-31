# from .models import KouryakuPost
from django.views.generic import ListView,TemplateView,DetailView,DeleteView
from .models import KouryakuPost,Comment,AdminUpdate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import KouryakuPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CommentCreateForm,KouryakuPostForm

# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'orderby_records'
    queryset = KouryakuPost.objects.order_by('-posted_at')


# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreateKouryakuView(CreateView):
    form_class = KouryakuPostForm
    template_name = "post.html"
    
    # データベースへの登録完了後のリダイレクト先
    success_url = reverse_lazy('kouryakuapp:post_done')

    def form_valid(self, form):
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        return super().form_valid(form)

class CommentSuccessView(TemplateView):
    template_name="comment_success.html"

class PostSuccessView(TemplateView):
    template_name ='post_success.html'

class KouryakuPostDetailView(DetailView):
    model = KouryakuPost
    template_name = "detail.html"
    context_object_name = "object" 

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "comment.html"

    success_url = reverse_lazy('kouryakuapp:comment_done')

    def form_valid(self, form):
        post = KouryakuPost.objects.get(pk=self.kwargs['pk'])  # 投稿を取得
        form.instance.target = post  # コメントの対象記事をセット
        form.instance.user_name = self.request.user  # ログインユーザーをセット
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('kouryakuapp:detail', kwargs={'pk': self.kwargs['pk']})  # 投稿詳細ページへリダイレクト

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = KouryakuPost.objects.get(pk=self.kwargs['pk'])  # `post` を渡す
        return context
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('kouryakuapp:detail', kwargs={'pk': self.object.target.pk})

    def test_func(self):
        """コメント投稿者のみ削除可能にする"""
        comment = self.get_object()
        return self.request.user == comment.user_name
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = KouryakuPost
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy('kouryakuapp:index')  # 削除後はトップページへリダイレクト

    def test_func(self):
        """投稿者のみ削除可能にする"""
        post = self.get_object()
        return self.request.user == post.user
    
class MypageView(ListView):
    template_name ='mypage.html'

    def get_queryset(self):
        queryset = KouryakuPost.objects.filter(user=self.request.user).order_by('-posted_at')
        return queryset

class CategoryView(ListView):
    template_name = "index.html"

    def get_queryset(self):
        # self.kwargsでキーワードの辞書を取得し、
        # categoryキーの値(Categorysテーブルのid)を取得
        category_id = self.kwargs["category"]
        # filter(フィールド名=id)で絞り込む
        categories = KouryakuPost.objects.filter(category=category_id).order_by("-posted_at")
        return categories

class UserView(ListView):
    template_name = "index.html"

    def get_queryset(self):
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs["user"]
        # filter(フィールド名=id)で絞り込む
        user_list = KouryakuPost.objects.filter(user=user_id).order_by("-posted_at")
        return user_list
    
class PostSearchView(ListView):
    model = KouryakuPost
    template_name = "post_search.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return KouryakuPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)  # タイトルまたは本文に含まれる
            )
        return KouryakuPost.objects.none()
    
class AdminUpdateListView(ListView):
    model = AdminUpdate
    template_name = "admin_update_list.html"
    context_object_name = "updates"
    ordering = ["-info_at"] 

class IndexView(ListView):
    model = KouryakuPost
    template_name = "index.html"
    context_object_name = "orderby_records"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["updates"] = AdminUpdate.objects.order_by("-info_at")[:5]  # 最新5件を取得
        return context