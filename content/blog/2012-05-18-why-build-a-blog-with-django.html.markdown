Title: "Why Build a Blog with Django?"
Tags: Django

This question comes up a lot, both in flame wars and in rational discussion.  Why would you take time to build a blog application with Django when there are engines like WordPress that do the same thing out of the box.  Well it depends.

The number one reason I think people choose Django to build a blog is because they want to learn Django.  Blogs are relatively straight forward animals.  They have an author, a title, and some sort of content.  They usually appear in chronological order on an index page of some kind, and if you're feeling feisty, that might even have "tags."

But why else?  Yes, I built my blog with Django to learn Django, but I keep it that way because I can literally modify it in any way I please.  I am not dependent on a bucket of "plugins" that may or may not have the functionality I desire.  For example, let's say I have a typical blog model that looks like this:

```python
class Entry(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:detail', [self.slug])
```

First, I'd like to point out how easy that was to make.  Second, assume I decide I want my blog to post to Twitter everytime I write a new entry.  Rather than digging for a WordPress plugin that may or may not do what I want, I can just override my save method:

```python
published_to_twitter = models.BooleanField(default=False)

def save(self, **kwargs):
    import twitter
    api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    api.PostUpdate('%s http://example.com%s' % (self.title, self.get_absolute_url()))
    self.published_to_twitter = True
    super(Entry, self).save(**kwargs)
```

Done, and I have full control over what is going on.  From the RSS feed, to the way my blog is displayed in a list view, and a detail view, to what comment engines I want to use, to how I want my blog to be tagged and/or categorized to collaboration, _I am in control._

Of course, that may not appeal to everyone, and I'll grant that no amount of internal control can trump the content you post.  But I say if you have the ability, Django is the way to go.  The learning curve is not as steep as you think, and it gives you a level of intimacy with your blog that you would not otherwise have.
