Title: The State of ember-django-adapter
Tags: Django REST Framework, Ember, ember-django-adapter
Summary: An increase in development activity has been taking place in the ember-django-adapter world.  Here's a quick update.

## Current Version (0.4.x)

[ember-django-adapter][] enables users to write applications using Django REST Framework and Ember.js.

### ember-cli support

In June, [I decided](https://github.com/toranb/ember-data-django-rest-adapter/issues/89) to extend @toranb's original [ember-data-django-rest-adapter][] by creating an ember-cli addon.  Basically, this involved grabbing the javascript dist files and bundling them into an npm-installable package.  This now exists as [ember-django-adapter][] which can be installed in your ember-cli project via:

```
npm install --save-dev ember-django-adapter
```

There are a few extra perks in the addon, such as blueprints for generating customizable adapter/serializer extensions.

## Version 1.0 (in progress)

Since ember-cli [is the future](https://github.com/emberjs/rfcs/blob/ember-2.0-rfc/active/0000-the-road-to-ember-2-0.md#big-bets) of Ember.js, we decided to move the entire codebase into the addon repository.

We are currently working toward a version 1.0 release of the adapter.  I've been working with [@benkonrath][] and [@holandes22][] to address outstanding issues and sort out documentation.

There are a few notable changes/improvements coming in version 1.0.

### New test runner

The new codebase in 1.0 will use the [addon test framework](http://www.ember-cli.com/#testing-the-addon-with-qunit) provided by ember-cli.

### Support Django REST Framework >= 3.0

Some of the changes in DRF 3.0 along with changes in recent versions of Ember Data have simplified a lot of the work that needs to be done by the adapter.  Because ember-cli is still somewhat bleeding edge, we decided to focus on DRF 3.0, and opt out of supporting 2.x.

For any users that this affects, I highly recommend upgrading to 3.0 if possible.  @tomchristie put a tremendous amount of work into making the upgrade path as smooth as possible, and the improvements are well worth it.

### Pagination

Version 1.0 will support pagination; usage examples to follow.

## Roadmap and Contributing

We plan to launch version 1.0 early in 2015.  Please feel free to join the conversation either on GitHub or in IRC (#ember-django-adapter in Freenode).  Testers and pull requests are always welcome.  Check out the [version-1.0 branch](https://github.com/dustinfarris/ember-django-adapter/tree/version-1.0) for more details.


[ember-django-adapter]: https://github.com/dustinfarris/ember-django-adapter
[ember-data-django-rest-adapter]: https://github.com/toranb/ember-data-django-rest-adapter
[@benkonrath]: https://github.com/benkonrath
[@holandes22]: https://github.com/holandes22
