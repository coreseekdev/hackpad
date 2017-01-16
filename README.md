# About LibrePad

LibrePad is a web-based realtime wiki, based on the open source HackPad document editor which based on the open source EtherPad collaborative document editor.


The etherpad package is distributed under the Apache License, Version 2.0.

All other packages are redistributed under their original license terms.  See below for a license summary of redistributed software.  More comprehensive license information can be found in the documentation of each package.

This document contains licensing information relating to the use of free and open-source software (FOSS) with or within the Hackpad software.  The authors, licensors, and distributors of the FOSS disclaim all express or implied conditions, representations, and warranties relating to the FOSS and any liability arising from use and distribution of the FOSS.

This document identifies the FOSS packages used in the Hackpad software, the FOSS licenses that Dropbox believes govern those FOSS packages.  While Dropbox has sought to provide complete and accurate licensing information for each FOSS package, Dropbox does not represent or warrant that the licensing information provided herein is correct or error-free.  Recipients of the Hackpad software should investigate the identified FOSS packages to confirm the accuracy of the licensing information provided herein.  Recipients are also encouraged to notify Dropbox of any inaccurate information or errors found in these notices.

# Runing

> python t_server.py

After running the server,
- visited http://localhost:5000/html/home , see the Login Page.
- http://localhost:5000/ see the demo of pads list.

# Not working

LibrePad is at very early stage, most of the features are misfunctional.

In HackPad, they used ejs template system, all the html building blocks make a mess and used a strange JVM based JS engine.
In LibrePad, I use Jinja2 as the template Engine, and a simple python web framework, Flask as the backend.

[X] Welcome Page
[X] List Pads Page
[X] Pad Editor (/pad/<pad_name>)

# TODO

[ ] Change the Jinja2 template into React
[ ] Adopt modern node.js building system, Gulp, Grunt, etc
[ ] Support Full Hackpad's API / URL Routing
[ ] Upgrade ACE to the lastest version
[ ] Add the Comet back ( Websockets, whatever)


# NOTICE

I do NOT want to involve any database into backend, use plain text instead.