Title: "Site Updates"
Tags:

I just finished a pretty big round of revisions on dustinfarris.com.
Included in this makeover:

  * Started using [SASS](http://sass-lang.com/) for my style edits. Coupled with [django-compressor](https://github.com/jezdez/django_compressor), which has a built-in preprocessor to compile edits on the fly, my CSS is more intuitive than ever.
  * Major HTML5 refactoring. Although it may not be obvious from the outside, I pretty much gutted the entire markup and rewrote it with cleaner, and more accurate semantics.
  * Implemented [microdata](http://schema.org/) accross the site for SEO and exploratory purposes.
  * Upgraded to [Django 1.4](https://www.djangoproject.com/). (previously on 1.4a)
  * Installed dcramer's [Sentry](https://github.com/dcramer/sentry) server to log errors and [Raven](https://github.com/dcramer/raven) for detection (and_loving_ it!)
  * Design updates--notice the new and improved background, sidebar, and search widget.

I plan on releasing the source to the public soon. Still
making minor tweaks and updating documentation, after which it is my hope that
this project will serve as a useful example of a small site to anyone who is
interested in learning about Django.
