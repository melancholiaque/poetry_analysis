from django.core.management.base import BaseCommand, CommandError
from ...models import Poet, Poem
from os.path import splitext
import pandas as pd
from tqdm import tqdm


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
        for author, content in tqdm(zip(df['author'], df['content']),
                                 total=len(df)):
            name = ' '.join([i.lower().capitalize() for i in author.split()])
            poet, _ = Poet.objects.get_or_create(name=name)
            Poem.objects.get_or_create(content=content, poet=poet)
