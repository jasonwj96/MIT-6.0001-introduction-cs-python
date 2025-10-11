# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, " ")
        words = text.split()
        clean_text = " ".join(words)
        return f" {self.phrase} " in f" {clean_text} "


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        fmt = "%d %b %Y %H:%M:%S"
        est = pytz.timezone("EST")
        self.time = est.localize(datetime.strptime(time_str, fmt))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate()
        if story_time.tzinfo is None:
            story_time = pytz.timezone("EST").localize(story_time)
        return story_time < self.time


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate()
        if story_time.tzinfo is None:
            story_time = pytz.timezone("EST").localize(story_time)
        return story_time > self.time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8

class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1, self.t2 = t1, t2

    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1, self.t2 = t1, t2

    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return [story for story in stories if any(t.evaluate(story) for t in triggerlist)]


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    trigger_file = open(filename, 'r')
    lines = [line.strip() for line in trigger_file if line.strip() and not line.startswith('//')]
    trigger_map = {}
    triggers = []

    for line in lines:
        parts = line.split(',')
        if parts[0] == "ADD":
            for name in parts[1:]:
                triggers.append(trigger_map[name])
        else:
            name, trigger_type = parts[0], parts[1]
            if trigger_type == "TITLE":
                trigger_map[name] = TitleTrigger(parts[2])
            elif trigger_type == "DESCRIPTION":
                trigger_map[name] = DescriptionTrigger(parts[2])
            elif trigger_type == "AFTER":
                trigger_map[name] = AfterTrigger(parts[2])
            elif trigger_type == "BEFORE":
                trigger_map[name] = BeforeTrigger(parts[2])
            elif trigger_type == "NOT":
                trigger_map[name] = NotTrigger(trigger_map[parts[2]])
            elif trigger_type == "AND":
                trigger_map[name] = AndTrigger(trigger_map[parts[2]], trigger_map[parts[3]])
            elif trigger_type == "OR":
                trigger_map[name] = OrTrigger(trigger_map[parts[2]], trigger_map[parts[3]])
    return triggers


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END,
                            "\n---------------------------------------------------------------\n",
                            "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END,
                            "\n*********************************************************************\n",
                            "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
