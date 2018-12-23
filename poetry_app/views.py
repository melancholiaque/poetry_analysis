from django.shortcuts import render
from django.views import View
from .services import pipeline
from .models import Poem
from random import choice


pipe = pipeline.load_from('pickled_objects/estimator.pkl')


class Home(View):

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {'poet': None, 'poem': None})

    def post(self, request):
        poem = request.POST.get('poem', None)
        if poem:
            poet = pipe.predict(poem)[0]
            poem = choice(Poem.objects.filter(poet__name=poet))
            return render(request, self.template_name,
                          {'poet': poet, 'poem': poem})
