Title: "Installing Ruby on Mountain Lion/MacPorts"
Tags: MacPorts RVM

If you use MacPorts, the following should get Ruby installed and working on your machine.

### Install RVM

Taken from the [RVM website][1]:

    curl -L https://get.rvm.io | bash -s stable --ruby

### Install OpenSSL and libyaml

    sudo port install openssl libyaml

### (Re)Install Ruby

    rvm reinstall 1.9.3 --with-openssl-dir=/opt/local --with-opt-dir=/opt/local

[1]: https://rvm.io/rvm/install/
