from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class AllMyIdeas(TemplateView):

    def get_context_data(self, **kwargs):
        pass