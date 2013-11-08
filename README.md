Dosage
======

"Keep your Tv Series dose going"

A tool that let's you download and keep tracking your favourite tv series. 
Also providing a Junky mode in wich the program tries to download the series chapters in a way that allows you to see all of them in a row.

Usage
------

Start tracking a tv series::

    python dosage.py --track "Mad Men"

stop tracking a tv series::

    python dosage.py --untrack "Mad Men" 

Setup a tv series in Yonky Mode::
   
    python dosage.py --junky "Breaking Bad"

Try it
-----

Before the release date (17/11/2013) you can try and test dosage, it has some bugs, doing this:

Start transmission and enable the rpc client in edit/preference then go to the web tab and click en "Enable Web Client"

Then you download and start the dosagedaemon

    git clone git@github.com:jairot/dosage.git
    virtualenv dosage
    cd dosage
    source bin/activate
    pip install -r requirements.txt
    cd src
    python dosagedaemon.py start

then you can add any tv series using the commands above.
    


