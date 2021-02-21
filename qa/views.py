from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from .models import Question, Answer, User
from .forms import AnswerForm, QuestionForm, CustomUserCreationForm, CustomUserChangeForm

#main_page
class QuestionListView(ListView):
    paginate_by = 10
    template_name = 'qa/main.html'

    def get_queryset(self):
        if self.request.GET.get('sort') == 'new':
            return Question.objects.new()
        if self.request.GET.get('sort') == 'popular':
            return Question.objects.popular()
        print(self.request.session)
        return Question.objects.new()


#question_details
class QuestionDetailsView(ListView):
    paginate_by = 5
    template_name = 'qa/question_detail.html'

    def get(self, request, *args, **kwargs):
        self.id = kwargs['id']
        try:
            self.question = Question.objects.get(id=self.id)
        except Question.DoesNotExist:
            return Http404
        return super().get(request, *args, **kwargs)

    def post (self, request, id):
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = form.save(id, request.user)
            url = reverse('question_details', kwargs={'id': id})
            return HttpResponseRedirect(url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        form = AnswerForm()
        context.update({
            'question': self.question,
            'form': form,
        })
        return context

    def get_queryset(self):
        if self.request.GET.get('sort') == 'new':
            return Answer.objects.new().filter(question__id=self.id)
        if self.request.GET.get('sort') == 'popular':
            return Answer.objects.popular().filter(question__id=self.id)
        return Answer.objects.filter(question__id=self.id)


#question_create
class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#user_create
class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'qa/user_form.html'
    success_url = reverse_lazy('login')


#profile_look
class ProfileLookView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'account'














