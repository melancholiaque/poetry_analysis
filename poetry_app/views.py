from django.shortcuts import render
from django.views import View
from .services import pipeline
from .models import Poem
from random import choice


try:
    pipe = pipeline.load_from('pickled_objects/estimator.pkl')
except FileNotFoundError:
    print('you running app without estimator '
          'create one with "python manage.py train_and_serialize'
          ' pickled_objects/estimator.pkl"')


class Home(View):

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name,
                      {'poet': None, 'poem': None})

    def post(self, request):
        poem = request.POST.get('poem', None)
        if poem and all(c in 'qwertyuiopasdfghjklzxcvbnm'
                      for c in filter(str.isalpha, poem)):
            poet = pipe.predict(poem)[0]
            poem = choice(Poem.objects.filter(poet__name=poet))
            return render(request, self.template_name,
                          {'poet': poet, 'poem': poem})
        return render(request, self.template_name,
                      {'poet': None, 'poem': None})
