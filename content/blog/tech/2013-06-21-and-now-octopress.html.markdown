Title: And now, Octopress
Tags: [Octopress]

![Octopress logo](/uploads/images/octopress.png)

What can top hosting your blog on GitHub Pages using Jekyll?  Wrapping it all together with Octopress.

Octopress is an open-source blogging framework that wraps the above
technologies in a nice package complete with automation in a Rakefile, a boilerplate theme, and lots of plugins.

But I didn't decide to use Octopress for the themes; in fact, I spent half a day gutting what it came with and dropping in bootstrap and my own design.  Where octopress shines is in its integration with Jekyll and GitHub.

GitHub has a rather annoying (but probably necessary) stipulation on using Jekyll and their Pages to host your blog: [No plugins allowed][].  I'm sure there are a hundred security reasons for this, but it makes doing, well, really anything outside of the Jekyll "box" impractical.

Octopress overcomes this roadblock by pre-compiling everything on your local machine before you deploy.  With this strategy, you can use any and whatever automation/plugin tools you like.  I, for one, am using a [tagging plugin][].  Oh, and SASS is built in too!

I cloned Octopress and made several changes to the HTML layout and CSS.  It is available on [GitHub][repo].

[No plugins allowed]: https://help.github.com/articles/pages-don-t-build-unable-to-run-jekyll#unsafe-plugins
[tagging plugin]: https://github.com/robbyedwards/octopress-tag-pages
[repo]: https://github.com/dustinfarris/dustinfarris.github.com/tree/source
