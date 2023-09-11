from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from app.cases.idea_exchange.idea import IdeaCase


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)


class AllMyIdeas(LoginRequiredMixin, TemplateView):

    template_name = 'my_ideas.html'

    def get_context_data(self, **kwargs):
        ctx = super(AllMyIdeas, self).get_context_data(**kwargs)
        case = IdeaCase()
        ctx['ideas'] = case.user_ideas(author_id=self.request.user.id)
        return ctx

class IdeaCreate(LoginRequiredMixin, FormView):

    template_name = 'idea_create.html'

    class CreateIdeaForm(forms.Form):
        body = forms.CharField()
        name = forms.CharField()
        chain_id = forms.ChoiceField(choices=[])

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


    form_class = CreateIdeaForm

    def get_context_data(self, **kwargs):
        ctx = super(IdeaCreate, self).get_context_data(**kwargs)
        case = IdeaCase()
        ctx['ideas'] = case.create_idea()
        return ctx

    def form_valid(self, form):
        case = IdeaCase()
        case.create_idea(
            user_id=self.request.user.id,
            body=form.cleaned_data['body'],
            chain_id=form.cleaned_data['chain_id'],
            name=form.cleaned_data['name']
        )
        return super(IdeaCreate, self).form_valid(form)