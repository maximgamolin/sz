from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.dll.idea_exchange.uow import IdeaUOW


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)


class AllMyIdeas(LoginRequiredMixin, TemplateView):

    template_name = 'my_ideas.html'

    def get_context_data(self, **kwargs):
        ctx = super(AllMyIdeas, self).get_context_data(**kwargs)
        uow = IdeaUOW()
        ctx['ideas'] = uow.all_user_ideas(self.request.user.id)
        return ctx
