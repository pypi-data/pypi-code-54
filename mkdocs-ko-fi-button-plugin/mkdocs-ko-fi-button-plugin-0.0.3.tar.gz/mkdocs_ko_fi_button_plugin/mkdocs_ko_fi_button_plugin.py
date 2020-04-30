import sys
import string
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class KofiButtonPlugin(BasePlugin):

    config_scheme = (
            ('id', config_options.Type(str)),
            ('type', config_options.Type(str, default='widget')),
            ('color', config_options.Type(str, default='#29abe0')),
            ('text', config_options.Type(str, default='Support Me on Ko-fi')),
            ('javascript_path', config_options.Type(str, default='widgets/widget_2.js')),
            ('javascript_f1', config_options.Type(str, default='kofiwidget2.init')),
            ('javascript_f2', config_options.Type(str, default='kofiwidget2.draw'))
    )

    def on_page_markdown(self, markdown, **kwargs):
        plugin_name = "ko-fi-button"
        tag = "{{ko-fi}}"
        hex_length = 6
        image_dict = {'blue': 'kofi1.png', 'bluegray': 'kofi2.png', 'red': 'kofi3.png', 'green': 'kofi4.png', 'black': 'kofi5.png'}

        for config in ['id', 'type', 'color', 'text', 'javascript_path', 'javascript_f1', 'javascript_f2']:
            # Check for non-existing config values.
            if not self.config[config]:
                sys.exit("Config '{}' is missing for {} plugin.".format(config, plugin_name))
            else:
                # Strip whitespace from all config values
                self.config[config] = self.config[config].strip()

                # Check for empty config values
                if self.config[config] == '':
                    sys.exit("The value of config '{}' is empty for {} plugin.".format(config, plugin_name))

        # Check the type config
        if not self.config['type'] in ["widget", "image"]:
            sys.exit("Incorrect value of config 'type' for {} plugin.".format(plugin_name))

        # Check the color config
        if self.config['type'] == "widget":
            # Temporarily remove the '#' from the color hex
            self.config['color'] = self.config['color'].replace('#', '')

            # Check the lenght of the color value
            if len(self.config['color']) != hex_length:
                sys.exit("Incorrect length of config 'color' for {} plugin.".format(plugin_name))

            # Check if the color value is hexadecimal
            if not all(c in string.hexdigits for c in self.config['color']):
                sys.exit("Config 'color' is not a hexadecimal value for {} plugin.".format(plugin_name))

            # Prepend the color hex with '#'
            self.config['color'] = "#" + self.config['color']
        else:
            if self.config['color'] not in ["blue", "bluegray", "red", "green", "black"]:
                self.config['color'] = "bluegray"
                #sys.exit("Incorrect value of config 'color' for {} plugin.".format(plugin_name))

        # Look for the Ko-fi markdown {{ko-fi}} and replace it
        if self.config['type'] == "widget":
            markdown = markdown.replace(tag, "<script type='text/javascript' src='https://ko-fi.com/{}'></script><script type='text/javascript'>{}('{}', '{}', '{}');{}();</script>".format(self.config['javascript_path'], self.config['javascript_f1'], self.config['text'], self.config['color'], self.config['id'], self.config['javascript_f2']))
        else:
            markdown = markdown.replace(tag, "<a href='https://ko-fi.com/{}' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/{}?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>".format(self.config['id'], image_dict[self.config['color']]))

        return markdown

