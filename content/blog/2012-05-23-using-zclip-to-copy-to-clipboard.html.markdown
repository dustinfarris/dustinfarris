Title: "Using zClip to 'Copy to Clipboard'"
Tags:

I've begun using django-filer to manage site assets after years of trying to beat a square peg (django-filebrowser) through a round hole (everything else).  It's been a very rewarding transition.

Part of the addiction to filebrowser was due to its integration with django-tinymce.  A long time ago, the maker of django-tinymce added a hook+widget for django-filebrowser and users have been complaining ever since.  Despite its shortcomings, though, people such as myself have continued using it because of the "this is the only way I can add images to my editor without uploading them somewhere else" mentality.

Recently, however, django-tinymce and I have [gone our separate ways](http://dustinfarris.com/2012/5/goodbye-tinymce/) leaving me with the freedom to choose a new editor, and a new way to manage media.  Enter django-filer.

[Django-filer](https://github.com/stefanfoulis/django-filer) is a great alternative to django-filebrowser featuring a cleaner interface and plenty of extra bells an whistles.  I now use it to upload my assets before writing a blog.  The hard part, I found, was getting the URL of uploaded assets.  I decided to [fork](https://github.com/dustinfarris/django-filer) the project and add a copy-to-clipboard function using the zClip library.

[zClip](http://www.steamdev.com/zclip/) allows you to set up an event hook on any HTML element that copies given text to the clipboard by overlaying the element with a Flash movie.

In this case, I used a span container for positioning, and then a nested span element to act as the widget:

```django
<span style="position:relative">
    <span class="zclip" data-copy="{{ file.url }}"></span>
</span>
```

Activating the widget is accomplished by adding a simple jQuery snippet in the <code>&lt;head&gt;</code>.

```javascript
$(document).ready(function() {
$('span.zclip').zclip({
    path: "flash/ZeroClipboard.swf",
    copy: function() {
            return $(this).attr('data-copy');
    },
    afterCopy: function() {
            $(this).fadeOut(100, function() {
                $(this).show();
            }
    }
});
});
```

To make it work properly I had to add some CSS:

```css
span.zclip {
    position: absolute;
    top: 0;
    left: 0;
    width: 16px;
    height: 16px;
    background: url('../img/clip.png') no-repeat;
}
```

Voila, I can quickly upload images and grab the URL making the disconnect from filebrowser even less bothersome:
![Screenshot of copy to clipboard](http://dustinfarris.com/media/filer/2012/05/23/screen_shot_2012-05-23_at_35113_pm.png)
