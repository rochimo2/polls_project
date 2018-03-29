from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    
    url(r'^pregunta/nuevo/$', views.QuestionPost, name='post_url'),
    
    url(r'^choice_update_form/$', views.ChoicePost, name='choice_update_form'),
    
    url(r'^ingreso/$', views.PaginaIngreso, name="ingreso"),
    
    url(r'^egreso/$', views.PaginaEgreso, name="egreso"),
    
    url(r'^registro/$', views.PaginaRegistro, name="registro"),
    
    url(r'^pregunta/editar/(?P<question_id>[0-9]+)$', views.EditarPregunta, name='question_update_form'),
    
    url(r'^pregunta/eliminar/(?P<question_id>[0-9]+)$', views.EliminarPregunta, name='eliminar pregunta'),
]