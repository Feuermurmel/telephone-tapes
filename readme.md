# telephone-tapes

A script to generate podcast feeds to listen to the _Telephone Tapes_ by _Evan Doorbell_ as they are listed on sub-pages of [Evan Doorbell's Phone Tapes](http://www.evan-doorbell.com).

The script will download the web-page from the passed URL generate one or multiple podcast feeds by looking at the raw HTML sources of the page. This builds on a lot of heuristics on how the formatting on these pages is done and thus might break whenever the page is updated. It has been tested on 2022-04-06 on these two pages:

http://www.evan-doorbell.com/production/group1.htm \
http://www.evan-doorbell.com/production/


## Setting up the Application in a Virtualenv

```
git clone https://github.com/Feuermurmel/telephone-tapes.git
cd telephone-tapes
python3 -m venv venv
venv/bin/pip install -e .
```


## Generating the Feeds

This will generate a single feed for the [Group 1 Playlist](http://www.evan-doorbell.com/production/group1.htm) and one feed for each group of recordings from the [Production Tapes](http://www.evan-doorbell.com/production/).

```
mkdir -p ../Telephone_Tapes/Group_1_Playlist 
mkdir -p ../Telephone_Tapes/Production_Tapes
venv/bin/tapes -o ../Telephone_Tapes/Group_1_Playlist http://www.evan-doorbell.com/production/group1.htm
venv/bin/tapes -o ../Telephone_Tapes/Production_Tapes/ http://www.evan-doorbell.com/production/
```
