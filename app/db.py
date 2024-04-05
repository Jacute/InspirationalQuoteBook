from .models import CustomUser, Quote, Category, QuoteCategory
from django.db import connection
from ast import literal_eval


def addQuote(quote: dict, isCustom=False):
    if isCustom:
        quoteItem = Quote(quote=quote['quote'], quote_author=quote['quoteAuthor'], suggester_author=quote['suggesterAuthor'], status=1) # quote adding
    else:
        quoteItem = Quote(quote=quote['quote'], quote_author=quote['quoteAuthor'], status=2)
    quoteItem.save()
    
    for category in quote['categories']:
        if not Category.objects.filter(category=category).exists():
            categoryItem = Category(category=category) # category adding
            categoryItem.save()
        else:
            categoryItem = Category.objects.get(category=category)
            
        link = QuoteCategory(quote=quoteItem, category=categoryItem) # quote and category link adding
        link.save()


def addQuotes(quotes: list):
    for quote in quotes:
        addQuote(quote)


def getQuotes(author=None, category=None, query=None, suggesterAuthor=None, isPub=True) -> list:
    quotes = Quote.objects
    
    if isPub:
        quotes = quotes.filter(status=1) # only publicated

    if author:
        quotes = quotes.filter(quote_author=author)
    if query:
        quotes = quotes.filter(quote__icontains=query)
    if category:
        category_id = Category.objects.get(category=category).id
        quote_ids = list(QuoteCategory.objects.filter(category=category_id).values_list('quote', flat=True))
        quotes = quotes.filter(id__in=quote_ids)
    if suggesterAuthor:
        suggesterAuthorId = int(CustomUser.objects.get(username=suggesterAuthor).id)
        quotes = quotes.filter(suggester_author=suggesterAuthorId)

    quotes = list(quotes.values())
    
    for i in range(len(quotes)):
        id = quotes[i]['id']
        category_ids = list(QuoteCategory.objects.filter(quote=id).values_list('category', flat=True))
        categories = list(Category.objects.filter(id__in=category_ids).values_list('category', flat=True))
        quotes[i]['categories'] = categories
    
    return quotes


def getQuotesBySuggester(suggester: str) -> list:
    quotes = Quote.objects.filter(suggester_author=suggester)


def getRandomQuotes(count: int) -> list:
    cur = connection.cursor()
    
    cur.execute(f"SELECT * FROM quotes WHERE status=1 ORDER BY RAND() LIMIT {count};")

    randomQuotes = list(map(lambda x: {'quote': x[1], 'author': x[2]}, cur.fetchall()))
    
    cur.close()
    
    return randomQuotes


def getCategories(author=None) -> list:
    if author:
        quote_ids = list(Quote.objects.filter(quote_author=author, status=1).values_list('id', flat=True))
        
        categorie_ids = list(QuoteCategory.objects.filter(quote__in=quote_ids).values_list('category', flat=True))
        categories = list(Category.objects.filter(id__in=categorie_ids).values_list('category', flat=True))
    else:
        categories = list(Category.objects.all().values_list('category', flat=True))
    categories.sort()
    
    return categories
    

def getAuthors(category=None) -> list:
    if category:
        category_id = Category.objects.get(category=category).id
        quote_ids = list(QuoteCategory.objects.filter(category=category_id).values_list('quote', flat=True))
        
        authors = list(Quote.objects.filter(id__in=quote_ids, status=1).values_list('quote_author', flat=True))
    else:
        authors = list(Quote.objects.filter(status=1).values_list('quote_author', flat=True))
    
    authors.sort()
    
    return authors


def clearTables():
    cur = connection.cursor()
    
    cur.execute('DELETE FROM quotes;')
    cur.execute("DELETE FROM sqlite_sequence WHERE name='quotes';")
    
    cur.execute('DELETE FROM users;')
    cur.execute("DELETE FROM sqlite_sequence WHERE name='users';")
    
    cur.close()