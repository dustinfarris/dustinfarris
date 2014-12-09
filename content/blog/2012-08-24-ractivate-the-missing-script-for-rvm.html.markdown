Title: "&quot;ractivate&quot;, the Missing Script for RVM"
Tags: RVM

When developing multiple projects in Ruby using [RVM][1], I've found that it can be difficult to keep track of which binaries and gemsets you are using, and installing gems to the wrong gemsets can cause problems.  Inspired by [virtualenv][2], I've created (largely copied) a script to switch between gemsets as you move between projects while developing in Ruby.

Instructions are for OSX, but the script can be used on any UNIX-based operating system.

Create a file in your home directory called ``.ractivate``, and paste this code:

```bash
deactivate() {
    if [ -n "$_OLD_VIRTUAL_PATH" ] ; then
        PATH="$_OLD_VIRTUAL_PATH"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi

    if [ -n "$_OLD_VIRTUAL_PS1" ] ; then
        PS1="$_OLD_VIRTUAL_PS1"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi

    if [ -n "$_RUBY_PROJECT_DIR" ] ; then
        rvm gemset use default
        unset _RUBY_PROJECT_DIR
    fi

    unset RUBY_PROJECT_DIR
    if [ ! "$1" = "nondestructive" ] ; then
        unset -f deactivate
    fi
}

# unset irrelavent variables
deactivate nondestructive

_RUBY_PROJECT_DIR="`pwd`"
export _RUBY_PROJECT_DIR

_OLD_VIRTUAL_PATH="$PATH"
PATH="$_RUBY_PROJECT_DIR/bin:$PATH"
export PATH

rvm gemset use `basename "$_RUBY_PROJECT_DIR"`

_OLD_VIRTUAL_PS1="$PS1"
if [ "x" != x ] ; then
    PS1="$PS1"
else
    PS1="(`basename \"$_RUBY_PROJECT_DIR\"`) $PS1"
fi
export PS1

# vim: ft=config
```

Create an alias for the script in ``.profile`` (also found in your home directory).

```bash
alias ractivate='source ~/.ractivate'
```

The idea is to create/use gemsets that _match the directory name_ of your Ruby project.  Ex:

![Ractivate](/media/filer/2012/08/24/ractivate.jpg "Ractivate in action")

[1]: https://rvm.io/
[2]: http://www.virtualenv.org/en/latest/index.html
