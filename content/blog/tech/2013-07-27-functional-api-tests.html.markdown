Title: Functional API Tests
Tags: Django

Little is more frustrating than running your test suite and watching it fail fail fail because insert name here’s API service is lagging/down/changed/throttled. While knowing about those things has importance, the time to learn about them isn’t when you’re trying to deploy a completely unrelated feature.

## Mocking to the rescue!

There are many libraries available in all languages worth a damn that allow you to short-circuit HTTP requests and insert a mock response; and your code is none the wiser. I’m particularly impressed with [HTTPretty][] that you can use right in your test:

```python
@httpretty.activate
def test_some_awful_api(self):
     httpretty.register_uri(
          httpretty.GET,
          "http://awful-api.com/action-foo-bar",
          body='{"success": false}',
          status=500,
          content_type='text/json')

     response = requests.get("http://awful-api.com/action-foo-bar")

     self.assertEqual({'success': False}, response.json())
     self.assertEqual(500, response.status_code)
```

You can always be assured of getting the same response back regardless of awful-api’s current mood.

## Great! Functional tests too?

No. So far every attempt on my part to integrate HTTPretty (or any other HTTP mocking library) with anything Selenium-related has ended either in a crash, or an unresponsive state. I’m assuming this is related to the monkey-patching these libraries do to the core Python libraries which interrupts communication with Selenium’s web driver as a side-effect.

## But wait! Do we really need to mock in this case?

No! And it took me a few days of hair-pulling to finally accept this. I ended up recording all of the responses from the API I’m polling (LinkedIn) and just bypassed the call altogether when testing. Essentially, in ``selenium_test_settings.py``:

```python
# Why Django doesn't support runtime environments out
# of the box yet is beyond me
ENVIRONMENT = 'test'
```

and in some file somewhere else (like in a fixtures module):

```python
responses = {
     "foo-bar-action": {
          "id": 12345,
          "attitude": "cool",
     },
}
```

and finally in the actual API code:

```python
def run_api_command(command):
     if settings.ENVIRONMENT in ['test']:
          return responses[command]
     else:
          response = requests.get("%s/%s" % (BASE_URL, command))
          return response.json()
```

I’m not a fan of modifying code just to accommodate tests. In my view, code should be, as much as possible, test agnostic. But in this case I see no other way and it has made my life less stressful which is a good thing.


[HTTPretty]: https://github.com/gabrielfalcao/HTTPretty
