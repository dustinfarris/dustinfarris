Title: From Django to GitHub Pages
Tags: Django, GitHub Pages, Jekyll, Markdown

I finally joined the cool club of hackers who host their blogs on [GitHub Pages][].  I won't rave
about the sheer awesomeness of using GitHub, [Jekyll][], and [Markdown][] to write blogs because
there are already about a hundred million other blogs out there doing just that.  I will, though,
mention a thing or two about migrating my blog from its previous framework, Django.

## Migrating Entries

Jekyll's required layout is well-defined, so to get a bunch of database stuff to look like
Markdown, I found it was easiest to run them all through a templating script that I wrote for just
the purpose.

The template is fairly straight-forward ``post.html``:

{% raw %}
``` django
Title: "{{ entry.title }}"
Date: {{ entry.pub_date|date:"Y-m-d H:i:s" }}

{{ entry.content|safe }}
```
{% endraw %}

The migration script was a little tricky because some of my posts were stored in Markdown already,
but some older ones were actually still in raw HTML from way-back-when I used a WYSIWYG editor.

I used an open-source convertor called [html2text][] with minimal issues.

The migration script converts anything written prior to May, 2012 and runs it through html2text.

```python
from django.template import Context, Template
from django.template.defaultfilters import slugify
from django.utils import timezone
import html2text

from blog.models import Entry


posts_dir = "~/Sites/dustinfarris.github.com/_posts"


def run():
    print "Starting..."
    template = Template(open('post.html').read())
    count = 0
    # The day I started using Markdown in Django
    md_started = timezone.get_default_timezone()
    for entry in Entry.objects.all():
        print "Migrating '%s'..." % entry.title
        pub_date = timezone.make_naive(entry.pub_date, default_timezone)
        if pub_date < md_started:
            entry.content = html2text.html2text(entry.content)

        # Open a new file using Jekyll's required naming format
        format = "{dir}/{date}-{slug}.md"
        filename = format.format(
            dir=posts_dir,
            date=entry.pub_date.strftime("%Y-%m-%d"),
            slug=slugify(entry.title))
        f = open(filename, 'w')

        # Render the template and encode in UTF-8 (just in case)
        context = Context({'entry': entry})
        content = template.render(context).encode('utf-8')

        # Done
        f.write(content)
        f.close()
        count += 1

    print "Finished migrating %d entries." % count
```

That took care of the heavy lifting, and I was left to tidy up the remains as I saw fit.

## Bash Script

In case this blogging setup isn't hackerish enough, I wrote a quick bash script to jumpstart a new
blog post.  In ``~/.profile``:

```bash
# Create a new blog post with boilerplate front-matter
function blog() {
  shopt -s xpg_echo
  cd ~/Sites/dustinfarris.github.com/_posts
  SLUGIFIED="$(echo -n "$1" | sed -e 's/[^[:alnum:]]/-/g' | tr -s '-' | tr A-Z a-z)" ;
  FILENAME="$(echo `date +\%Y-\%m-\%d`-$SLUGIFIED)" ;
  TIMESTAMP="$(echo `date +\%Y-\%m-\%d` `date +\%H:\%M:\%S`)" ;
  echo "---\n\nlayout: default\ntitle: \"$1\"\ndate: $TIMESTAMP\n\n---\n\n" > $FILENAME.md ;
  vi +":set syntax=markdown" + $FILENAME.md ;
}
```

Now if I can just find an editor that doesn't go berserk on embedded code blocks.


[GitHub Pages]: http://pages.github.com/
[Jekyll]: http://jekyllrb.com/
[Markdown]: http://daringfireball.net/projects/markdown/
[html2text]: https://github.com/aaronsw/html2text
