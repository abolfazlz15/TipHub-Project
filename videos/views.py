from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, View
from .models import Category, Comment, Like, Notification, Video
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = "videos/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(status=True).order_by('-created')
        context['top_videos'] = context['videos'].order_by('-view')
        return context


class VideoListView(ListView):
    model = Video
    context_object_name = 'videos'
    paginate_by = 1
    template_name = 'videos/all-videos.html'


class VideoDetailView(View):
    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, slug=kwargs['slug'])
        _list = Comment.objects.filter(video=video, parent=None)
        paginator = Paginator(_list, 3)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)

        # get user ip for view
        ip_address = request.user.ip_address
        if ip_address not in video.view.all():
            video.view.add(ip_address)

        # like system
        if request.user.is_authenticated:
            if request.user.likes.filter(video__slug=kwargs['slug'],
                                         user_id=request.user.id).exists():  # if user like article show in templates
                is_liked = True
            else:
                is_liked = False
        else:
            is_liked = False

        context = {
            'video': video,
            'comments': comments,
            'is_liked': is_liked,
        }
        return render(request, 'videos/video-detail.html', context)

    def post(self, request, *args, **kwargs):
        # comment system
        video = get_object_or_404(Video, slug=kwargs['slug'])
        parent_id = request.POST.get('parent_id')
        text = request.POST.get('text')
        comment = Comment.objects.create(video=video, user=request.user, text=text, parent_id=parent_id)
        # add notification when user send comment
        if parent_id:  # If a user replies to another user's comment, the first user will be notified
            Notification.objects.create(sender_user=request.user, geter_user=comment.parent.user,
                                        text=f'کاربری به {comment.parent.text} پاسخ داد', link=video.get_absolute_url())

        Notification.objects.create(sender_user=request.user, geter_user=video.teacher.user,
                                    text=f'کاربری به {video.title} کامنتی ثبت کرد', link=video.get_absolute_url())
        return redirect('videos:video-detail', video.slug)


class DeleteNotificationView(View):
    def get(self, request, id):
        notification = Notification.objects.get(id=id)
        notification.delete()
        return redirect(notification.link)


class LikeView(View):
    def get(self, request, pk):
        video = get_object_or_404(Video, id=pk)
        if request.user.is_authenticated:
            try:
                like = Like.objects.get(video_id=pk, user_id=request.user.id)
                like.delete()
                return JsonResponse({"status": "unlike", "count": video.likes.count()})
            except:
                Like.objects.create(video_id=pk, user_id=request.user.id)
                return JsonResponse({"status": "liked", "count": video.likes.count()})
        return redirect('videos:video-detail', video.id)


class SearchVideoView(ListView):
    model = Video
    template_name = 'videos/all-videos.html'
    paginate_by = 1
    context_object_name = 'videos'

    def get_queryset(self):
        videos = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            return Video.objects.filter(
                Q(title__icontains=q) |
                Q(teacher__user__full_name__icontains=q) |
                Q(description__icontains=q)
            ).filter(status=True)
        return videos


class FavoriteVideoList(ListView):
    model = Like
    template_name = 'videos/favorite_video_list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Like.objects.filter(user=self.request.user)

        return queryset


class CategoryList(ListView):
    paginate_by = 1
    template_name = 'videos/all-videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        id = self.kwargs['id']
        category = get_object_or_404(Category, id=id)
        return category.videos.all()
