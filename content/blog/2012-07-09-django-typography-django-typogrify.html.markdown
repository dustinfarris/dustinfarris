Title: "Django + Typography = django-typogrify"
Tags: Django

Something I've put off dealing with (until today) is typography.  As a little bit of history: the typewriter forced us to sacrifice certain printed media standards because of its monospaced font.  Things like double-spacing between sentences and using straight quotes can be considered typewriter-era "hacks" so this portable machine could sort of mimic what the printing presses were doing.

Well a lot of these hacks have become habitual and, for some, even typing "law"--how many people know there should only be [one space][1] between sentences?  Well, thanks to the advancement of technology, we can break these habits and return to the glory days of beautiful text.

In Django, this means server-side substitution.  Since there are not separate open-quotes/close-quotes keys on my keyboard, and especially since I use [markdown][2] to draft my writings, something needs to process the text and make the appropriate replacements.  Enter [django-typogrify][3].

django-typogrify with the help of a [smartypants][4] Python port does a lot, most significantly:

* Converts straight quotes to "curly" quotes
* Converts three dots into ellipsis
* Converts dashes into hyphens, en dashes, and em dashes
* Prevents "widowed" one-word lines as a result of word wrapping

It does a lot more than that, but those are the main points I'm using.  I had a small caveat because I usually write my em dashes as " -- ".  Note the surrounding spaces.  I've learned that this is actually bad grammar; there should be no spaces when writing an em dash.  Thankfully, Django and Python make this an easy fix:

```python
  from blog.models import Entry
  import re

  for e in Entry.objects.all():
      e.content = re.sub(r'(\w) -- (\w)', r'\1--\2', e.content)
      e.save()
```

There is plenty more typography work to do here.  django-typogrify does a lot of class-wrapping for various grammatical entities which need to be styled.  I also need to take a look at my font choices from a "big picture" point of view and determine if they are working well together.  Smashing Magazine plenty of [material][5] on that.  All in all, though, django-typogrify has given my blog a nice kick in the typographic pants.

[1]: http://en.wikipedia.org/wiki/Sentence_spacing
[2]: http://dustinfarris.com/2012/5/goodbye-tinymce/
[3]: https://github.com/chrisdrackett/django-typogrify/
[4]: http://daringfireball.net/projects/smartypants/
[5]: http://www.smashingmagazine.com/tag/typography/
