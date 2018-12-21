from django.core.management.base import BaseCommand, CommandError
from ...models import Poet, Poem
from os.path import splitext
import pandas as pd


class Command(BaseCommand):

    help = 'parses csv into db'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str,
                            help='.csv file to read from')

    def handle(self, *args, **options):
        path = options.get('path', None)
        if not path:
            raise CommandError('Path not provided')
        if splitext(path)[-1] != '.csv':
            raise CommandError('Provide a .csv file')
        df = pd.read_csv(path)
        for author, poem_name, age, content in zip(df['author'],
                                                df['poem name'],
                                                df['age'],
                                                df['content']):
            name = ' '.join([i.lower().capitalize() for i in author.split()])
            poet, _ = Poet.objects.get_or_create(name=name)
            Poem.objects.get_or_create(content=content, name=poem_name,
                                       age=age, poet=poet)
