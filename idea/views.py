from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from app.cases.idea_exchange.idea import IdeaCase, ChainCase


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

class IdeaView(LoginRequiredMixin, TemplateView):

        template_name = 'idea.html'
        # TODO: Доделать шаблон

        def get_context_data(self, **kwargs):
            ctx = super(IdeaView, self).get_context_data(**kwargs)
            case = IdeaCase()
            ctx['idea'] = case.fetch_idea(idea_uid=kwargs['idea_uid'])
            return ctx

class IdeaCreate(LoginRequiredMixin, FormView):

    template_name = 'idea_create.html'
    # TODO: Доделать шаблон

    class CreateIdeaForm(forms.Form):
        body = forms.CharField()
        name = forms.CharField()
        chain_id = forms.ChoiceField(choices=[])

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            chain_case = ChainCase()
            self.fields['chain_id'].choices = [
                (i.chain_id, f'Chain: {i.chain_id}') for i in chain_case.fetch_allowed_chains()
            ]


    form_class = CreateIdeaForm


    def form_valid(self, form):
        case = IdeaCase()
        idea = case.create_idea(
            user_id=self.request.user.id,
            body=form.cleaned_data['body'],
            chain_id=form.cleaned_data['chain_id'],
            name=form.cleaned_data['name']
        )
        return HttpResponseRedirect(redirect_to=reverse('idea:idea', kwargs={'idea_uid': idea.get_idea_uid()}))