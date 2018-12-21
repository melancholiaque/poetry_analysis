from django.shortcuts import render
from django.views import View
from .services import predict
from .models import Poem
from random import choice


class Home(View):

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {'poet': None, 'poem': None})

    def post(self, request):
        poem = request.POST.get('poem', None)
        if poem:
            poet = predict(poem)[0]
            poem = choice(Poem.objects.filter(poet__name=poet))
            return render(request, self.template_name,
                          {'poet': poet, 'poem': poem})
