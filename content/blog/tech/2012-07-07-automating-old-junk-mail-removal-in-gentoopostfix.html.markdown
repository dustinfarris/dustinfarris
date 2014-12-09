Title: "Automating Old Junk-mail Removal in Gentoo/Postfix"
Tags:

I run a mail server on a typical Linux/Postfix/Amavisd/Dovecot stack and have been recently playing with sa-learn.  More on that later.  In the mean-time I thought I'd share a quickie bash command to remove old junk mail from all virtual users that I just spun up in a cron job:

```console
find /var/mail/ -regextype posix-extended -regex '.*Junk/(cur|new)/.*' -ctime 14 -exec rm {} \;
```

Of note is the ``-regextype`` flag.  Apparently, [find][1] uses emacs style regex parsing by default which doesn't allow "or" groups.  Ok, I'm really going to sleep now.

[1]: http://linux.die.net/man/1/find
