import urllib2
import praw
import re
import sys
import os
import json

class Pulse(object):
    def __init__(self, page):
        self.page = page
        print page
        self.last_comment_id = None
        self.reddit = praw.Reddit('thangs')
        self.submission = self.reddit.get_submission(page, comment_sort='new')
        self.title = str(self.submission.title).replace(' ','_').replace(
            '-','').replace(':','').replace('~','').replace('(','').replace(
            ')','')[0:32]
        print self.title
        self.gdt_file ='%s.txt' % os.path.join(os.path.expanduser('~'), self.title)
        self.pulse_dict = {}
        self.uniques = set()
        self.comment_ids = set()
        self.read_shit()

        
    def run(self):
        self.submission.replace_more_comments(limit=None, threshold=0)
        all_comments = self.submission.comments
        flat_comments = praw.helpers.flatten_tree(all_comments)
        self.outstring_header = ("team|fucks|c\\\\_ass|posts by team|users by flair"
                            "\n---------|---------|---------|----------|----------")
        self.outstring_template = "{team}|{fucks}|{_class}|{by_team}|{by_flair}"        

        self.fuck = re.compile('fu*ck')
        self._class = re.compile('class.*')

        self.latest_comment_id = flat_comments[0].id
        print self.latest_comment_id
        print self.last_comment_id
        
        for idx, comment in enumerate(flat_comments):
            print comment.id
            if comment.id in self.comment_ids:
                continue
            self.comment_ids.add(comment.id)
            self.go(comment)
            if (idx % 100) == 0:
                self.print_shit()

        self.print_shit(done=True)
        print 'finished. %s comments processed' % idx

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
            
        if str(comment.author) not in self.uniques:
            self.uniques.add(str(comment.author))
            self.pulse_dict[aft]['unique'] += 1
            
        self.pulse_dict[aft]['count'] += 1

    def print_shit(self, done=False):
        print ('\n' * 50)
        outstring = "\n".join(self.outstring_template.format(
        team=k, fucks=x['fucks'], _class=x['class'],
        by_team=x['count'], by_flair=x['unique']) for k,x in
        self.pulse_dict.iteritems())
        if done:
            print 'Writing to %s' % self.gdt_file
            with open(self.gdt_file, 'wb') as p:
                p.write(json.dumps(self.pulse_dict) + '\n')
                p.write('Comment: %s' % self.latest_comment_id + '\n')
                p.write(json.dumps(list(self.uniques)) + '\n')
                p.write(json.dumps(list(self.comment_ids)) +  '\n')
                p.write(self.outstring_header + '\n')
                p.write(outstring)
        print self.outstring_header
        print outstring

    def read_shit(self):

        try:
            with open(self.gdt_file, 'rb') as p:
                print 'Reading from %s' % self.gdt_file
                json_dict = p.readline()
                self.pulse_dict = dict(json.loads(json_dict))
                comment = p.readline()
                if comment.startswith('Comment'):
                    self.last_comment_id = comment.split(' ')[1]
                self.uniques = set(json.loads(p.readline()))
                self.comment_ids = set(json.loads(p.readline()))
        except Exception, e:
            print e
            print 'No file found'

print 'GDT address?'
page = str(raw_input("> "))


parser = Pulse(page)
parser.run()

