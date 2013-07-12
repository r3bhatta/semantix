Semantix
========

The Semantix crawler.

Installation
------------

1. Install Python 2.7.3.
2. Install [Flask](http://flask.pocoo.org/docs/installation/ "Flask"). Make sure `virtualenv` is 
installed. Follow the instructions to install to activate the virtual environment and flask.
3. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/ "BeautifulSoup").
4. Install [NLTK](http://nltk.org/install.html "NLTK").

Run
---

1. Run `./start`.

Notes
-----

We activate a virtual environment to ensure our project runs on the enclosed Python version and is 
not affected by the other Python versions installed on the machine. Flask is also installed into 
the virtual environment, and not globally on our machine.

OCR Recognition
---------------

OCR recognition is done using the Tesseract library.

1. brew install tesseract  

Usage:  
    `tesseract [image_name] [output_file]`
