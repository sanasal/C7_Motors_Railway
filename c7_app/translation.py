from modeltranslation.translator import translator, TranslationOptions
from .models import Article

class ArticleTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'header',
        'read_more',
    )

translator.register(Article, ArticleTranslationOptions)