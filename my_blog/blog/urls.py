from django.conf.urls import url
from blog import views

app_name = 'blog'


urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^register/',views.register,name='register'),
    url(r'^after_register/',views.AfterRegister.as_view(),name='after_register'),
    url(r'^after_login/(?P<pk>\d+)/$',views.after_login,name='after_login'),
    url(r'^about/',views.AboutPage.as_view(),name='about'),
    url(r'^contact/',views.ContactPage.as_view(),name='contact'),
    url(r'^author/(?P<pk>\d+)/posts/$',views.author_posts,name='author_posts'),
    url(r'^post_detail/(?P<pk>\d+)/$',views.PostDetailView.as_view(),name='post_detail'),
    url(r'^post/(?P<pk>\d+)/comments/$',views.post_comments,name='post_comments'),
    url(r'^user/(?P<pk>\d+)/write_post/',views.write_post,name='write_post'),
    url(r'^post/(?P<pk>\d+)/write_comment/',views.write_comment,name='write_comment'),
    # url(r'^user/(?P<pk>\d+)/save_draft/',views.save_draft,name='save_draft'),
    url(r'^user/(?P<pk>\d+)/drafts/',views.user_drafts,name='user_drafts'),
    url(r'^user/(?P<pk>\d+)/draft_detail/',views.user_draft_detail,name='user_draft_detail'),
    url(r'^user/(?P<pk>\d+)/draft_publish/',views.publish_post,name='publish_post'),
    url(r'^post/(?P<pk>\d+)/delete/',views.delete_post,name='delete_post'),
    url(r'^post/(?P<pk>\d+)/update/',views.UpdatePost.as_view(),name='update_post'),












]
