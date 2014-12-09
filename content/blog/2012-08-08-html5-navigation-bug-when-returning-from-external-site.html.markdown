Title: "HTML5 Navigation Bug When Returning From External Site"
Tags: HTML5

So HTML5 navigation is in full swing, and it's awesome.  If you aren't implementing it yet, start.  I found a bug in Chrome, though, (and possibly other browsers) that resulted in your JSON data being grossly displayed as a webpage if the user visited and returned from an external site.

It appears that Chrome caches the AJAX response from the HTML5 navigation as the complete content for that particular URL.  To overcome this, add a dummy GET parameter:

```javascript
$('a').on('click', function() {
    url = $(this).attr('href');
    $.get(
        url + "?dontcache=1",
        function(response) {
            history.pushState(
                {'content': response.content},
                response.title,
                url
            );
            ...
```

Of course, if you're already using GET parameters in your link URLs there's the issue of appending parameters to parameters which involves [more regex][1] than this post deserves.

[1]: http://stackoverflow.com/questions/486896/adding-a-parameter-to-the-url-with-javascript
