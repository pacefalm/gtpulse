import urllib2
import praw
import re
import sys
import os

class Pulse(object):
    pass
      

class PageParse(object):
    def __init__(self, page):
        self.page = page
        print page
        self.reddit = praw.Reddit('thangs')
        self.submission = self.reddit.get_submission(page)
        self.pulse_dict = {}
        self.uniques = []
        
    def run(self):
        self.submission.replace_more_comments(limit=None, threshold=0)
        all_comments = self.submission.comments
        flat_comments = praw.helpers.flatten_tree(all_comments)
        self.outstring_header = ("team|fucks|c\\\\_ass|posts by team|users by flair"
                            "\n---------|---------|---------|----------|----------")
        self.outstring_template = "{team}|{fucks}|{_class}|{by_team}|{by_flair}"        

        self.fuck = re.compile('fu*ck')
        self._class = re.compile('class.*')

        """while True:
            print flat_comments[1]

            if len(flat_comments) == 0:
                break"""
        for idx, comment in enumerate(flat_comments):
            self.go(comment)
            if (idx % 100) == 0:
                self.print_shit()

        self.print_shit(done=True)
        print 'finished. %s comments processed' % idx

        "self.submission.replace_more_comments()"
            

        ":fucks = get_fucks(comment)"

        """outstring = "\n".join(outstring.format(
            team=k, fucks=x['fucks'], _class=x['class'],
            by_team=x['count'], by_flair=x['unique']) for k,x in
            self.pulse_dict.iteritems())"""
        
        
        """print "Number of fucks by flair:  "
        for k,v in self.pulse_dict.iteritems():
            print "%s:\t%s  " % (k,v['fucks'])
        print " "
        print "Number of unique users by flair:"
        for k,v in self.pulse_dict.iteritems():
            print "%s:\t%s  " % (k,v['unique'])
        print " "
        print "Number of posts by flair:  "

        for k,v in self.pulse_dict.iteritems():
            print "%s:\t%s  " % (k,v['count'])
        print " "
        print "Number of unique users: %s" % len(self.uniques)"""

    def go(self, comment):
        try:
            aft = comment.author_flair_text[0:3]
        except:
            aft = 'None'
        if aft not in self.pulse_dict:
            self.pulse_dict[aft] = {
                'fucks' : 0,
                'count' : 0,
                'unique' : 0,
                'class' : 0
                }
        if self.fuck.search(comment.body.lower()):
            self.pulse_dict[aft]['fucks'] += 1
        if self._class.search(comment.body.lower()):
            self.pulse_dict[aft]['class'] += 1
            
        if comment.author not in self.uniques:
            self.uniques.append(comment.author)
            self.pulse_dict[aft]['unique'] += 1
            
        self.pulse_dict[aft]['count'] += 1

    def print_shit(self, done=False):
        print ('\n' * 50)
        outstring = "\n".join(self.outstring_template.format(
        team=k, fucks=x['fucks'], _class=x['class'],
        by_team=x['count'], by_flair=x['unique']) for k,x in
        self.pulse_dict.iteritems())
        if done:
            with open('%s.txt' % self.page.split('/')[6], 'wb') as p:
                print >> p, self.outstring_header
                print >> p, outstring
        print self.outstring_header
        print outstring

print 'GDT address?'
page = str(raw_input("> "))


parser = PageParse(page)
parser.run()

