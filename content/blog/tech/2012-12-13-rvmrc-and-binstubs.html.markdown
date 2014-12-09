Title: ".rvmrc and binstubs"
Tags: RVM

A while ago I wrote a [script][1] to help manage gemsets and PATH settings when switching between Ruby projects.  It has worked very well, but I've recently learned about .rvmrc — yes, I'm still new at this.

Most RoR programmers probably know that one must prefix console commands with ``bundle exec`` to ensure the correct binaries are used for the project you are working on.  Something like:

```console
bundle exec rake db:test:prepare
```

Most RoR programmers also probably know that you can "stub" out these binaries into a project directory by installing your gems with:

```console
bundle install --binstubs=./bundler_stubs
```

So, the objective is to get the bundler_stubs directory on your system path whenever you are working on the project (and off your path when you leave it).

The ``.rvmrc`` file goes in your project's root directory and it is automatically sourced in the background when you enter the directory.  There is also an optional ``.rvmrc`` file in your home directory that gets called whenever you leave your project's root directory — or enter any other non-.rvmrc-containing directory for that matter.  The .rvmrc file is simply a [bash script][2], so without further ado, here is an .rvmrc file for your project that will switch to a project-specific gemset and place the project's bundler_stubs directory on your path.  You only need to edit the top line:

```bash
rvm --create ruby-1.9.3-p327@projectname

deactivate()
    if [ -n "$_OLD_VIRTUAL_PATH" ] ; then
    PATH="$_OLD_VIRTUAL_PATH"
    export PATH
    unset _OLD_VIRTUAL_PATH
    fi

    if [ -n "$_OLD_VIRTUAL_PS1" ] ; then
    PS1="#_OLD_VIRTUAL_PS1"
    export PS1
    unset _OLD_VIRTUAL_PS1
    fi

    unset _RUBY_PROJECT_DIR

    if [ ! "$1" = "nondestructive" ] ; then
    unset -f deactivate
    fi
}

# unset irrelevant variables
deactivate nondestructive

_RUBY_PROJECT_DIR="`pwd`"
export _RUBY_PROJECT_DIR
_OLD_VIRTUAL_PATH="$PATH"
PATH="$_RUBY_PROJECT_DIR/bundler_stubs:$PATH"
export PATH

_OLD_VIRTUAL_PS1="$PS1"
if [ "x" != x ] ; then
    PS1="$PS1"
else
    PS1="(`basename \"$_RUBY_PROJECT_DIR\"`) $PS1"
fi
```

This gives the ability to move in and out of your project's directory and your gemsets and PATH are managed seamlessly:

![.rvmrc script in action](/media/filer_public/2012/12/13/rvmscriptinaction.png)

[1]: http://dustinfarris.com/2012/8/ractivate-the-missing-script-for-rvm/
[2]: https://rvm.io/workflow/rvmrc/
