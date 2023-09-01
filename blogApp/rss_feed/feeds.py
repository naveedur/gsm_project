from django.contrib.syndication.views import Feed
from django.urls import reverse
from blogApp.models import article  # Import your article model
from django.utils.feedgenerator import Atom1Feed  # Import Atom1Feed for Atom feed

class ArticleFeed(Feed):
    title = "My Blog"
    link = "/blog/"
    description = "The latest news from my blog."

    def items(self):
        return article.objects.filter(verified=True)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc  # Use the 'desc' field from your model

    def item_link(self, item):
        return reverse('postpage', args=[item.slug])  # Use 'sno' as the identifier

    # # Define the pub_date for each item
    # def item_pubdate(self, item):
    #     return item.pub_date

    # # Use Atom feed format
    # feed_type = Atom1Feed