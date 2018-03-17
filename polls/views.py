"""Vistas de los modelos"""

from django.contrib.auth import authenticate, login, get_user_model,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


#from django.forms.models import inlineformset_factory
#Agrego import 3de febrero
from django.views.generic.edit import UpdateView, CreateView, FormView
from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm, IngresarForm, RegistrarForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. sin incluir las que tienen fecha futura"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionaste ninguna opción.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def ChoicePost(request):
    if request.method == 'POST':
        formulario = ChoiceForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect ('/polls')
    else:
        formulario = ChoiceForm()
    return render(request, 'polls/questionpost_form.html', {'formulario' : formulario})

def QuestionPost(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # ChoiceFormSet = inlineformset_factory(
        #     QuestionForm,
        #     ChoiceForm,
        #     fields=('choice_text'),
        #     extra= 3
        # )
        if form.is_valid():
            question = Question(
                question_text = form.cleaned_data['question_text'],
                pub_date = form.cleaned_data['pub_date']
                )
            question.save()
            return HttpResponseRedirect('/polls')
    else:
        form = QuestionForm()
    return render(request, 'polls/post_url.html', {'form' : form})

def EditarPregunta(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.question_text=form.cleaned_data['question_text']
            question.pub_date= form.cleaned_data['pub_date']
            question.save()
            return HttpResponseRedirect('/polls')
    else:
        form = QuestionForm({'question_text' : question.question_text, 'pub_date' : question.pub_date})
    return render(request, 'polls/question_update_form.html', {'form' : form, 'pregunta' : question})
        # return render(request, 'polls/question_update_form.html', {
        # 'question': question,
        # 'error_message': "No seleccionaste ninguna opción.",})

#para eliminar preguntas
def EliminarPregunta(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.question_text=form.cleaned_data['question_text']
            question.pub_date= form.cleaned_data['pub_date']
            question.delete()
            return HttpResponseRedirect('/polls')
    else:
        form = QuestionForm({'question_text' : question.question_text, 'pub_date' : question.pub_date})
    return render(request, 'polls/eliminar_pregunta.html', {'form' : form, 'pregunta' : question})

# class QuestionPost(CreateView):
#     model = QuestionForm
#     fields = ['question_text','pub_date']

# class QuestionPost(FormView):
#     template_name = 'polls/questionpost_form.html'
#     form_class = QuestionForm
#     success_url = '/polls/choice_update_form'

#     def form_valid(self, form):
#         form.postea_pregunta()
#         return super().form_valid(form)

# class ChoicePost(UpdateView):
#         form = ChoiceForm
#         fields = ['choice_text']
#         template_name_suffix = '_update_form'

# la página de inicio
def PaginaInicio(request):
    if request.user.is_autenticated():
        context["contenido_premium"] = "Yeah!"
    return render(request, "polls/index.html", {"context" : context})


# Login_page
def PaginaIngreso(request, pk=None, *args, **kwargs):
    form= IngresarForm(request.POST or None)
    contexto = {
            "form": form
        }
    # print("Usuario logged in")
    # print(request.user.is_autenticated())
    # print(request.user)
    if form.is_valid():
        print(form.cleaned_data)
        usuario = form.cleaned_data.get("usuario")
        contraseña = form.cleaned_data.get("contraseña")

        user = authenticate(request, username=usuario, password=contraseña)
        if user is not None:
            login(request, user)
            # contexto['form'] = IngresarForm()
            return redirect("/polls/")
        else:
            raise Http404("No existe el usuario. Porqué? No se...")
    return render(request, "polls/ingreso.html", contexto)

def PaginaEgreso(request, pk=None, *args, **kwargs):
    logout(request)
    # return HttpResponseRedirect(reverse('egreso', ))
    return redirect("/polls/ingreso")

# register_page
User = get_user_model()
def PaginaRegistro(request):
    form= RegistrarForm(request.POST or None)
    contexto = {
            "form": form
        }
    if form.is_valid():
        print(form.cleaned_data)
        usuario = form.cleaned_data.get("Usuario")
        email = form.cleaned_data.get("email")
        contraseña = form.cleaned_data.get("contraseña")
        nuevo_usuario = User.objects.create_user(usuario, email, contraseña)
        print(nuevo_usuario)

    return render(request, "polls/registro.html", contexto)

