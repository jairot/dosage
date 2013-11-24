TvDosage
======

"Keep your Tv Series dose going"

A tool that let's you download and keep tracking your favourite tv series. 
Also providing a Junky mode in wich the program tries to download the series chapters in a way that allows you to see all of them in a row.

Usage
------

Start the DosageDaemon:

    dosagedaemon start

Start tracking a tv series:

    tvdosage --track "Mad Men"

stop tracking a tv series:

    tvdosage --untrack "Mad Men" 

Setup a tv series in Junky Mode:

    tvdosage --junky "Breaking Bad"

Check all the available commands:

    tvdosage --help

Try it
-----

Try TvDosage!!. It only works on GNU/Linux environmet with the transmission torrent Client

first install the python environment tools:

    sudo apt-get install python-dev python-pip

Start transmission and enable the rpc client in edit/preference then go to the web tab and click en "Enable Web Client"

Then you download and start the dosagedaemon:

    sudo pip install tvdosage

then start the DosageDaemon:

    dosagedaemon start

then you can add any tv series using the commands above.
    
Do you test this Shit?
----------------------

[![Build Status](https://travis-ci.org/jairot/dosage.png?branch=master)](https://travis-ci.org/jairot/dosage)
