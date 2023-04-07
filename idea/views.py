from django.views.generic import TemplateView

from app.dll.idea_exchange.uow import IdeaUOW


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        uow = IdeaUOW()
        print(uow)
        return super(IndexView, self).get_context_data(**kwargs)


class AllMyIdeas(TemplateView):

    def get_context_data(self, **kwargs):
        pass