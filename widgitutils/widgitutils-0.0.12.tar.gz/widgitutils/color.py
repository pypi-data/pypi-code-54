from discord import Colour, TextChannel
from re import search
from redbot.core import commands


def color_from_hex(parent, ctx: commands.Context, color: str):
    """
    Helper to convert hex colors into Discord colors
    """

    return WidgitColor(parent).from_hex(ctx, color)


def format_color(parent, ctx: commands.Context, color: str):
    """
    Convert a color string to its appropriate Discord color
    """

    return WidgitColor(parent).format_color(ctx, color)


def get_valid_colors(parent):
    """
    Returns a dict containing the valid predefined colors.
    """

    return WidgitColor(parent).get_valid_colors()


class WidgitColor:
    def __init__(self, parent):
        self.parent = parent

        self.colors = {
            "teal": "#1abc9c",
            "dark_teal": "#11806a",
            "green": "#2ecc71",
            "dark_green": "#1f8b4c",
            "blue": "#3498db",
            "dark_blue": "#206694",
            "purple": "#9b59b6",
            "dark_purple": "#71368a",
            "magenta": "#e91e63",
            "dark_magenta": "#ad1457",
            "gold": "#f1c40f",
            "dark_gold": "#c27c0e",
            "orange": "#e67e22",
            "dark_orange": "#a84300",
            "red": "#e74c3c",
            "dark_red": "#992d22",
            "lighter_grey": "#95a5a6",
            "dark_grey": "#607d8b",
            "light_grey": "#979c9f",
            "darker_grey": "#546e7a",
            "blurple": "#7289da",
            "greyple": "#99aab5",
        }

    def from_hex(self, ctx: commands.Context, color: str):
        """
        Helper to convert hex colors into Discord colors
        """

        color = color.lstrip("#")

        if len(color) == 3:
            color = color + color

        if len(color) == 6 and search(r"^(?:[0-9a-fA-F]{3}){1,2}$", color):
            c1 = int(color[0:2], 16)
            c2 = int(color[2:4], 16)
            c3 = int(color[4:6], 16)

            return Colour.from_rgb(c1, c2, c3)

        return self._get_embed_color(ctx.channel)

    def format_color(self, ctx: commands.Context, color: str):
        """
        Convert a color string to its appropriate Discord color
        """

        if color in self.colors:
            return self.from_hex(ctx, self.colors[color])

        return self.from_hex(ctx, color)

    def get_valid_colors(self):
        """
        Returns a dict containing the valid predefined colors.
        """

        return self.colors

    def _get_embed_color(self, channel: TextChannel) -> Colour:
        """
        Return the default color for an embed
        """

        return self.parent.bot.get_embed_color(channel)
