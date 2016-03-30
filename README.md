# Scraping data from Gmail using Python
#### 28th March 2016
**The problem:** Realising that Amazon S3 (which I host my website on) does not support PHP and I need to host a form for a Language Acquisition experiment.

**The solution:** The pipeline I set up, which works as follows:

* Create a web form as you would normally using `input` HTML elements.
* Make it instantly awesome by using [formspree.io](http://formspree.io), which allows you to receive answers to your form directly to your inbox.
* Set up a filter in Gmail telling it to label emails from formspree and have them skip the inbox.
* Run the following Python script to harvest the data into a csv file.

*Note:* you will first need to sign up for and create an API instance from the Google Developers Console before being able to access Gmail programmatically as detailed here.

##### Preliminaries
First, we import a handful of modules which will allow us to deal with accessing a Gmail account, reading raw email (in base64) and writing a csv. We also load API keys from a .json file stored locally.

##### Functions provided

There are three functions in the script:
* `getCredentials()` is largely based off code provided by Google to interface with the API [here](https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample).
* `getLabel()` Will search for emails with the label specified by the variable `query`. It then fetches the id of those emails and returns a list of those id numbers, `l_id`.
* `getData()` first downloads the emails corresponding to the id numbers in `l_id`. It then searches through them with regexes to match the relevant data submitted by participants (*note:* enabling formspree's *plaintext* flag makes this part easier). Lastly, it writes a csv in which each line corresponds to the data given by a single participant.
