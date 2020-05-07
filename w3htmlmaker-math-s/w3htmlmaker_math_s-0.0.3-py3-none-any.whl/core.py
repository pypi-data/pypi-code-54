import re


class HtmlArticle:
    title = ""
    text_html = ""

    def __init__(self, text, title):
        self.text_html = text
        self.title = title.capitalize()
        self.make_p()
        self.make_title()
        self.make_container()

    def get_html(self):
        return self.text_html

    def make_container(self):
        self.text_html = "<div class=\"w3-container\">\n" + self.text_html + "</div>"

    def make_p(self):
        self.text_html = "\t<p>" + self.text_html.replace('\n', "</p>\n\t<p>") + "</p>"

    def make_quote(self):
        self.text_html = self.text_html.replace('\'', "&#8810")

    def make_title(self):
        self.text_html = "\t<h1>" + self.title + "</h1>\n" + self.text_html

    def make_header(self, text):
        text_header = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link rel=\"stylesheet\" href=\"https://www.w3schools.com/w3css/4/w3.css\">\n"
        return text_header + text

    def make_code(self):
        self.text_html = self.text_html.replace("<code>", "<div class=\"w3-panel w3-card w3-black \"><p>")
        self.text_html = self.text_html.replace("</code>", "</p></div> ")
