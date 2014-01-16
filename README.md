Semantix
========

The Semantix crawler - in progress.  

Implements a Naive Bayes classifier using the NLTK library.  

Takes in crawled HTML pages of a whole website and classifies the website based on a business type 
such as `restaurant` or `medical`.  

Based on the business type, further classify the website's content into relevant data such as hours 
of operation, location, and menu items for restaurants.


Installation
------------

1. Install Python 2.7.3.
2. Clone the project and navigate into it.
3. Install `virtualenv` and make sure it is activated. All Python libraries should be installed 
while `virtualenv` is activated.
4. Install [Flask](http://flask.pocoo.org/docs/installation/ "Flask").
5. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/ "BeautifulSoup").
6. Install [NLTK](http://nltk.org/install.html "NLTK").
7. Obtain crawled websites data from someone on the team.

Quick Installation Commands
---------------------------

1. Install Python 2.7.3.
2. `git clone https://github.com/rhuang/semantix.git`
3. `sudo pip install virtualenv`
4. `virtualenv venv`
5. `. venv/bin/activate`
6. `pip install -U Flask beautifulsoup4 pyyaml nltk`
7. `./start` or `python semantix.py`

Windows
-------

1. To run locally first start the environment by running `winStart.bat`
2. Then run `python semantix.py`
3. In your browser type `127.0.0.1:5001`

Mac
---

1. Run `./start`.

Notes
-----

We activate a virtual environment to ensure our project runs on the enclosed Python version and is 
not affected by the other Python versions installed on the machine. Flask is also installed into 
the virtual environment, and not globally on our machine.

You can also run `python app/main.py` to check out the main algorithms without starting flask.

OCR Recognition
---------------

OCR recognition is done using the Tesseract library.

1. `brew install tesseract`  

Usage:  
    `tesseract [image_name] [output_file]`
