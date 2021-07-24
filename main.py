#!/usr/bin/env python

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

import csv
import random
import re

#import vocab

def read_csv(fname='vocab.csv', delimiter=';', encoding='utf-8'):
    """Reads in vocabulary from custom csv file and returns as list"""

    vocab = []

    with open(fname, newline='', encoding=encoding) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter)
        for row in csvreader:
            vocab.append(row)
    return vocab


class RootWidget(BoxLayout):
    """RootWidget is the base Widget of this application.
    """

    lang1head = StringProperty('')
    lang2head = StringProperty('')
    wordtypes = ListProperty([])
    lessons = ListProperty([])

    def __init__(self, **kwargs):
        """Constructor method
        """

        super(RootWidget, self).__init__(**kwargs)

        # Load the vocabulary data
        vocabulary = read_csv()
        self.headers = vocabulary[0]
        self.base_vocabulary = vocabulary[1:]
        self.vocablist = self.base_vocabulary
        self.vocab = None


        # Sets
        wordtype_set = set(['All'])
        lesson_set = set(['All'])
        for i in self.vocablist:
            wordtype_set.add(i[2])
            lesson_set.add(i[3])

        # Populate variables to fill the labels
        self.lang1head = self.headers[0]
        self.lang2head = self.headers[1]

        self.wordtypes = sorted(list(wordtype_set))
        self.lessons = sorted(list(lesson_set))

        # Control variables

        # The direction of testing
        # 0 = lang1 to lang2; 1 = lang2 to lang1
        # acts as index in self.vocab
        self.langdir = 0

        # Selects the wordtype to test
        # All, verbs, nouns, adjectives, other
        self.wordtype = 'All'

        # Selects the lesson to test
        # All, 0, 1, 2, 3, etc.
        self.lesson = 'All'

    def remove_warning_label(self, dt):
        self.ids['warning_lbl'].text = ''

    def post_warning(self, msg):
        """
        Sets a settings warning label to msg.
        """
        self.ids['warning_lbl'].text = msg

    def quit_app(self):
        """Quits the app and closes it.
        """
        App.get_running_app().stop()

    def create_vocablist(self):
        """
        Creates a vocablist from self.base_vocabulary based on filter items.

        Taking all filters into account
        """

        self.wordtype = self.ids['td_wordtype'].text
        self.lesson = self.ids['td_spin'].text

        if self.wordtype == 'All' and self.lesson == 'All':
            self.vocablist = self.base_vocabulary
        elif self.wordtype == 'All':
            self.vocablist = [voc for voc in self.base_vocabulary
                              if voc[3] == self.lesson]
        elif self.lesson == 'All':
            self.vocablist = [voc for voc in self.base_vocabulary
                              if voc[2] == self.wordtype]
        else:
            self.vocablist = [voc for voc in self.base_vocabulary
                              if voc[2] == self.wordtype if voc[3] == self.lesson]

        # If vocabulary list is empty, reset to default and post warning
        if self.vocablist == []:
            msg = 'WARNING: With these filters, the vocabulary list is empty. Resetting to default.'
            self.post_warning(msg)
            self.reset_settings()
            Clock.schedule_once(self.remove_warning_label, 30)
            

    def reset_settings(self):
        """
        Resets the settings to default type
        """
        self.wordtype = 'All'
        self.ids['td_wordtype'].text = 'All'
        
        self.lesson = 'All'
        self.ids['td_spin'].text = 'All'

        self.vocablist = self.base_vocabulary

    def show_answer(self):
        """
        Shows the answer in the empty text box
        """
        if self.langdir:
            self.ids['txt_lang1'].text = self.vocab[self.langdir-1]
        else:
            self.ids['txt_lang2'].text = self.vocab[self.langdir+1]

    def switch_langdir(self):
        """
        Changes variable that decides which language will be tested.
        """

        if not self.langdir:
            self.ids['btn_langdir'].text = '<-'
            self.langdir = 1
        else:
            self.ids['btn_langdir'].text = '->'
            self.langdir = 0

    def test_vocab(self):
        """
        Choose a random vocabulary item and populate the chosen vocabulary.

        Do not show the other side.
        """

        # Activate the necessary widgets
        if self.ids['btn_next'].text == 'Start':
            self.ids['btn_next'].text = 'Next'

        if self.ids['btn_show'].disabled:
            self.ids['btn_show'].disabled = False

        # Choose a vocabulary item
        self.vocab = random.choice(self.vocablist)

        # Populate textboxes
        if self.langdir:
            self.ids['txt_lang1'].text = ''
            self.ids['txt_lang2'].text = self.vocab[self.langdir]
        else:
            self.ids['txt_lang1'].text = self.vocab[self.langdir]
            self.ids['txt_lang2'].text = ''


class VocabApp(App):
    """The kivy.app Child starting the construction.
    """

    def build(self):
        root = RootWidget()
        return root


if __name__ == '__main__':
    VocabApp().run()