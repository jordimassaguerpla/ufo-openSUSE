# Update Forecast for openSUSE Linux distribution

Inspired on https://sourceforge.net/projects/updateforecast/

This project is for getting a forecast of how many updates will be released of a set of packages in the openSUSE linux distribution.

The first step is to create an histogram of the current history.

For this, download the update-info.xml file from 

http://ftp5.gwdg.de/pub/opensuse/update/openSUSE-current/repodata/

and create a whitelist.json file for the set of packages (see examples directory)

and run

python histogram.py update-info.xml whitelist.json

Example output

https://github.com/jordimassaguerpla/ufo-openSUSE/blob/master/example_output.png

More will come, but for now we have the histogram

Enjoy



