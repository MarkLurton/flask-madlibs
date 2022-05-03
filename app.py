"""Madlibs Stories."""
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = 'letsgostros'
debug = DebugToolbarExtension(app)

class Story:
    """Madlibs story.

    To  make a story, pass a list of prompts, and the text
    of the template.

        >>> s = Story(["noun", "verb"],
        ...     "I love to {verb} a good {noun}.")

    To generate text from a story, pass in a dictionary-like thing
    of {prompt: answer, prompt:answer):

        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat a good mango.'
    """

    def __init__(self, words, text):
        """Create story with words and template text."""

        self.prompts = words
        self.template = text

    def generate(self, answers):
        """Substitute answers into text."""

        text = self.template

        for (key, val) in answers.items():
            text = text.replace("{" + key + "}", val)

        return text


# Here's a story to get you started

storyLibrary = {
    "once_upon_a_time"    : Story(["place", "noun", "verb", "adjective", "plural_noun"],
                                    """Once upon a time in a long-ago {place}, there lived a
                                    large {adjective} {noun}. It loved to {verb} {plural_noun}.""")
                            ,
    "years_in_the_future" : Story(["plural_noun", "verb", "time", "number", "famous_person"], """
                                    Years in the future, the world will be ran by {plural_noun}.
                                    Under their rule, it is illegal to {verb} after {time}. All households are 
                                    required to keep {number} portraits of {famous_person}.""")
                            ,
    "my_mom_taught_me"   :  Story(["verb", "plural_noun", "adjective", "noun", "song"], """My mom 
                                    taught me that you should never {verb} {plural_noun}. If you do, a {adjective} ghost will haunt 
                                    you until you give it a {noun} and sing {song}.""")
}

@app.route('/')
def home_page():
    """Home Page for Madlibs app"""
    return render_template("index.html")

@app.route('/form')
def form_page():
    """Form Page for Madlibs app"""
    story = storyLibrary[request.args['story-select']]
    return render_template("form.html", prompts=story.prompts, story_select=request.args['story-select'])

@app.route('/story')
def story_page():
    """Story Page for Madlibs app"""
    answers = request.args
    story = storyLibrary[request.args['story-select']]
    madlib = story.generate(answers)
    return render_template("story.html", madlib=madlib)
