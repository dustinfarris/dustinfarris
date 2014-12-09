Title: "Installing MongoDB with MacPorts on MountainLion"
Tags: MacPorts MongoDB

Technically this should be as simple as:

    :::console
    sudo port install mongodb

Unfortunately, the mongodb port depends (for now) on devel/boost <= 1.49.  The boost port was recently upgraded to 1.50, so to install db you will have to uninstall boost and explicitly reinstall it at version 1.49:

    :::console
    sudo port uninstall boost
    svn co -r 93341 http://svn.macports.org/repository/macports/trunk/dports/devel/boost/
    cd boost
    sudo port install

    sudo port -n install mongodb
