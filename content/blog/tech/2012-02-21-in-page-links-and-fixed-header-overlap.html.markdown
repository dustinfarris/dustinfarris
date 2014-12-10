Title: "In-page Links and Fixed Header Overlap"
Tags: CSS

Problem: You have a fixed position header (like the one on this page), and you
find that using `<a href="#othersection">` causes a portion of your document
to be "hidden" by the banner after being brought to the top of the page. From
a visual standpoint, when you declare `position:fixed` on an element, say a
div, the browser stops considering the div's dimensions when working with
other parts of the page layout. This is especially noticeable when you have an
in-page link and it scrolls underneath your banner. For example, if you have:


Click to jump to "section"

## Section

...

When you click the link to jump to `#section`, your h2, and possibly other
text, will be partially hidden by the header `div`. ![Fixed-header problem example](/media/uploads/fixedheader_example.png) The solution is to "trick"
the browser into thinking the jump point is higher than it really is. To make
this solution elegant, use a separate element (like span) when declaring the
jump point: :::html

## Section

...

Assuming the header's height is 70px, you must offset the jump point by at
least that much. Modify the span element with the following CSS:


```css
span.anchor { display: block; height: 70px; margin-top: -70px; visibility:
hidden; }
```


The browser will consider the height attribute when calculating
where to scroll to, and the negative top margin keeps any large gaps from
appearing in your page content. ![Fixed-header problem fixed example](/media/uploads/fixedheaderfixed_example.png) This solution works
well in all modern browsers.

  * CSS: Cascading Style Sheets
