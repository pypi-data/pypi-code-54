import asyncio
import datetime
from discord import Embed, Message, TextChannel, errors
from discord.embeds import EmptyEmbed
from re import search, sub
from redbot.core import commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from .color import get_valid_colors, format_color
from .format import valid_url


async def build_embed(parent, ctx: commands.Context, **kwargs):
    """
    Helper to determine whether or not an embed should be used.
    """

    return await WidgitEmbed(parent).build(ctx, **kwargs)


async def editor(
    parent,
    ctx: commands.Context,
    embed_id: str = None,
    channel: TextChannel = None,
    **kwargs,
):
    """
    Helper to build an embed editor.
    """

    return await WidgitEmbed(parent).editor(ctx, embed_id, channel, **kwargs)


class WidgitEmbed:
    def __init__(self, parent):
        self.parent = parent
        self.channel = None
        self.embed_data = {}
        self.embed_id = None
        self.msg = None
        self.original = {}
        self.editor_data = {
            "cog_name": "",
            "edit_type": {},
            "errors": [],
            "prompts": [],
            "responses": [],
            "inline": False,
            "options": None,
            "supported_desc": "",
            "the_editor": None,
        }

    async def build(self, ctx: commands.Context, **kwargs):
        """
        Helper to determine whether or not an embed should be used.
        """

        if commands.bot_has_permissions(embed_links=True):
            return await self._embed_msg(ctx, **kwargs)

        fallback = kwargs.get("post") or None

        if fallback:
            return await ctx.send(fallback)

        raise WidgitEmbedException(
            self.parent._(
                "I doesn't have permission to post embeds and no fallback post was given!"
            )
        )

    async def editor(
        self,
        ctx: commands.Context,
        embed_id: str = None,
        channel: TextChannel = None,
        **kwargs,
    ):
        """
        Embed editor.
        """

        edit_types = {
            "add": {"title": self.parent._("add"), "action": self.parent._("creation")},
            "edit": {
                "title": self.parent._("edit"),
                "action": self.parent._("editing"),
            },
        }

        fields = {
            "title": self.parent._("Title"),
            "url": self.parent._("URL"),
            "description": self.parent._("Description"),
            "footer": self.parent._("Footer Text"),
            "footer_icon": self.parent._("Footer Icon"),
            "thumbnail": self.parent._("Thumbnail"),
            "image": self.parent._("Image"),
            "color": self.parent._("Color"),
        }

        mandatory = {
            "preview": self.parent._("Preview"),
            "cancel": self.parent._("Cancel"),
        }

        mandatory_inline = {
            "save": self.parent._("Save"),
            "cancel": self.parent._("Cancel"),
        }

        self.editor_data["inline"] = kwargs.get("inline") or False
        self.embed_id = embed_id
        self.channel = channel or ctx.channel

        supported_fields = kwargs.get("supported") or fields
        supported = {}
        for field, field_name in fields.items():
            if field in supported_fields:
                supported[field] = field_name

        if self.editor_data["inline"]:
            for field, field_name in supported.items():
                self.editor_data["supported_desc"] += self.parent._(
                    "\n_{}. {}{}_"
                ).format(
                    list(supported.keys()).index(field),
                    self.parent._("Edit "),
                    field_name,
                )

            self.editor_data["supported_desc"] += "\n\n"

            for field, field_name in mandatory_inline.items():
                self.editor_data["supported_desc"] += self.parent._("{}`{}` ").format(
                    ":white_check_mark:"
                    if field == "save"
                    else ":negative_squared_cross_mark:",
                    field_name,
                )
        else:
            for field, field_name in supported.items():
                self.editor_data["supported_desc"] += self.parent._(
                    "\n_{}. {}_"
                ).format(list(supported.keys()).index(field), field_name)

            self.editor_data["supported_desc"] += "\n\n"

            for field, field_name in mandatory.items():
                self.editor_data["supported_desc"] += self.parent._("{}`{}` ").format(
                    ":white_check_mark:"
                    if field == "preview"
                    else ":negative_squared_cross_mark:",
                    field_name,
                )

        self.editor_data["edit_type"] = kwargs.get("type") or "add"
        self.editor_data["edit_type"] = edit_types[self.editor_data["edit_type"]]

        self.editor_data["cog_name"] = kwargs.get("cog") or self.parent._(
            "Embed Editor"
        )
        editor_title = self.parent._(
            "{} :: {} Embed".format(
                self.editor_data["cog_name"],
                self.editor_data["edit_type"]["title"].capitalize(),
            )
        )

        if self.editor_data["edit_type"]["title"] == "add":
            self.msg = await self.build(ctx, channel=channel)
        else:
            if not self.embed_id:
                return await ctx.send(
                    self.parent._("Cowardly refusing to edit a nonexistent message.")
                )

            if type(self.embed_id) is int:
                self.embed_id = str(self.embed_id)

            if type(self.embed_id) is Message:
                self.embed_id = str(self.embed_id.id)  # type: ignore

            if type(self.embed_id) is not str:
                return await ctx.send(
                    self.parent._("Cowardly refusing to edit a nonexistent message.")
                )

            if not self.embed_id.isdigit():
                return await ctx.send(
                    self.parent._("Cowardly refusing to edit a nonexistent message.")
                )

            try:
                self.msg = await self.channel.fetch_message(int(self.embed_id))
            except errors.NotFound:
                return await ctx.send(
                    self.parent._("Cowardly refusing to edit a nonexistent message.")
                )

            if len(self.msg.embeds) == 0:
                return await ctx.send(
                    self.parent._(
                        "Cowardly refusing to edit a message without an embed."
                    )
                )

        posted_embed = self.msg.embeds[0]

        if posted_embed.title:
            self.embed_data["title"] = posted_embed.title
            self.original["title"] = posted_embed.title

        if posted_embed.description:
            self.embed_data["description"] = posted_embed.description
            self.original["description"] = posted_embed.description

        if posted_embed.image.url:
            self.embed_data["image"] = posted_embed.image.url
            self.original["image"] = posted_embed.image.url

        if posted_embed.thumbnail.url:
            self.embed_data["thumbnail"] = posted_embed.thumbnail.url
            self.original["thumbnail"] = posted_embed.thumbnail.url

        if posted_embed.url:
            self.embed_data["url"] = posted_embed.url
            self.original["url"] = posted_embed.url

        if posted_embed.footer.text:
            self.embed_data["footer_text"] = posted_embed.footer.text
            self.original["footer_text"] = posted_embed.footer.text

        if posted_embed.footer.icon_url:
            self.embed_data["footer_icon"] = posted_embed.footer.icon_url
            self.original["footer_icon"] = posted_embed.footer.icon_url

        if posted_embed.color:
            self.embed_data["color"] = posted_embed.color
            self.original["color"] = posted_embed.color

        building = True

        if (
            self.editor_data["edit_type"]["title"] == "edit"
            and not self.editor_data["inline"]
        ):
            editor_description = self.parent._(
                "Select which embed component you would like to configure.\n{}".format(
                    self.editor_data["supported_desc"]
                )
            )

            self.editor_data["the_editor"] = await build_embed(
                self.parent, ctx, title=editor_title, description=editor_description,
            )
            self.embed_id = self.editor_data["the_editor"].id
        else:
            self.editor_data["the_editor"] = self.msg

            the_title = (
                self.embed_data["title"]
                if "title" in self.embed_data
                else self.editor_data["cog_name"]
            )
            the_description = (
                self.embed_data["description"]
                if "description" in self.embed_data
                else ""
            )

            posted_embed = self.msg.embeds[0]
            posted_embed.title = self.parent._(
                "{} :: {} Embed".format(
                    the_title, self.editor_data["edit_type"]["title"].capitalize()
                )
            )
            posted_embed.description = self.parent._("{}\n{}").format(
                the_description, self.editor_data["supported_desc"]
            )
            self.embed_data["title"] = posted_embed.title
            self.embed_data["description"] = posted_embed.description

            await self.msg.edit(embed=posted_embed)

        self.editor_data["options"] = ReactionPredicate.NUMBER_EMOJIS[: len(supported)]
        self.editor_data["options"] += ReactionPredicate.YES_OR_NO_EMOJIS

        try:
            start_adding_reactions(
                self.editor_data["the_editor"], self.editor_data["options"]
            )
        except errors.Forbidden:
            await self._cleanup(all=True)
            return await ctx.send(
                self.parent._("I'm not allowed to add reactions here!")
            )

        while building:
            try:
                the_options = [*self.editor_data["options"]]

                pred = ReactionPredicate.with_emojis(
                    the_options, self.editor_data["the_editor"], ctx.author
                )
                await ctx.bot.wait_for("reaction_add", check=pred, timeout=30)

                await self.editor_data["the_editor"].remove_reaction(
                    the_options[pred.result], ctx.author  # type: ignore
                )

                if supported and int(pred.result) < len(supported):  # type: ignore
                    selected = list(supported)[int(pred.result)]  # type: ignore
                if supported and int(pred.result) >= len(supported):  # type: ignore
                    result = int(pred.result) - len(supported)  # type: ignore

                    if self.editor_data["inline"]:
                        selected = list(mandatory_inline)[result]
                    else:
                        selected = list(mandatory)[result]

                if selected == "title":
                    await self._set_title(ctx)

                if selected == "url":
                    await self._set_url(ctx)

                if selected == "description":
                    await self._set_description(ctx)

                if selected == "footer":
                    await self._set_footer_text(ctx)

                if selected == "footer_icon":
                    await self._set_footer_icon(ctx)

                if selected == "thumbnail":
                    await self._set_thumbnail(ctx)

                if selected == "image":
                    await self._set_image(ctx)

                if selected == "color":
                    await self._set_color(ctx)

                if selected == "preview":
                    building = not await self._preview(ctx)

                    if not building:
                        await self._save(done=True)
                        await self._cleanup(all=True)

                if selected == "save":
                    await self._save(done=True)
                    await self._cleanup(all=True)
                    building = False

                if selected == "cancel":
                    await self._cleanup(all=True, cancel=True)
                    await ctx.send(
                        self.parent._("Embed {} cancelled.").format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                    building = False

                continue
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._("Embed {} timed out.").format(
                        self.editor_data["edit_type"]["action"]
                    )
                )

    async def _cleanup(self, **kwargs):
        """
        Editor cleanup script.
        """

        clean_all = kwargs.get("all") or False
        cancel = kwargs.get("cancel") or False
        preview = kwargs.get("preview") or False

        if clean_all:
            if self.editor_data["inline"]:
                await self.msg.clear_reactions()
            else:
                await self.editor_data["the_editor"].delete()

        if cancel:
            await self._save(cancel=True)

        if preview:
            await preview.delete()

        if len(self.editor_data["errors"]) > 0:
            for error in self.editor_data["errors"]:
                self.editor_data["errors"].remove(error)
                await error.delete()

        if len(self.editor_data["responses"]) > 0:
            for response in self.editor_data["responses"]:
                self.editor_data["responses"].remove(response)
                await response.delete()

        if len(self.editor_data["prompts"]) > 0:
            for prompt in self.editor_data["prompts"]:
                self.editor_data["prompts"].remove(prompt)
                await prompt.delete()

    async def _embed_msg(self, ctx: commands.Context, **kwargs):
        """
        Build and display an embed.
        """

        title = kwargs.get("title", EmptyEmbed) or EmptyEmbed
        _type = kwargs.get("type", "rich") or "rich"
        url = kwargs.get("url", EmptyEmbed) or EmptyEmbed
        description = kwargs.get("description", EmptyEmbed) or EmptyEmbed
        timestamp = kwargs.get("timestamp")
        footer = kwargs.get("footer") or kwargs.get("footer_text")
        footer_icon = kwargs.get("footer_icon")
        thumbnail = kwargs.get("thumbnail")
        image = kwargs.get("image")
        self.channel = kwargs.get("channel") or ctx.channel

        color = kwargs.get("colour") or kwargs.get("color") or None

        contents = dict(title=title, type=_type, url=url, description=description)

        embed = kwargs.get("embed") or EmptyEmbed
        embed = embed.to_dict() if hasattr(embed, "to_dict") else {}

        contents.update(embed)

        if timestamp and isinstance(timestamp, datetime.datetime):
            contents["timestamp"] = timestamp

        embed = Embed.from_dict(contents)

        embed.color = await self.parent.bot.get_embed_color(self.channel)

        if color and color != "unset":
            embed.color = color

        if color and color == "unset":
            embed.color = EmptyEmbed

        if footer:
            if footer_icon:
                embed.set_footer(text=footer, icon_url=footer_icon)
            else:
                embed.set_footer(text=footer)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if image:
            embed.set_image(url=image)

        return await self.channel.send(embed=embed)

    async def _preview(self, ctx: commands.Context):
        """
        Preview an embed.
        """

        embed_data = self.embed_data

        title = embed_data["title"] if "title" in embed_data else EmptyEmbed
        description = (
            embed_data["description"] if "description" in embed_data else EmptyEmbed
        )
        url = embed_data["url"] if "url" in embed_data else None
        color = embed_data["color"] if "color" in embed_data else None
        image = embed_data["image"] if "image" in embed_data else None
        thumbnail = embed_data["thumbnail"] if "thumbnail" in embed_data else None
        footer_text = embed_data["footer_text"] if "footer_text" in embed_data else None
        footer_icon = embed_data["footer_icon"] if "footer_icon" in embed_data else None

        preview = await self.build(
            ctx,
            title=title,
            description=description,
            image=image,
            url=url,
            thumbnail=thumbnail,
            footer_text=footer_text,
            footer_icon=footer_icon,
            color=color,
        )

        confirm = await ctx.send(self.parent._("Does this look right?"))
        self.editor_data["prompts"].append(confirm)

        try:
            start_adding_reactions(confirm, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(confirm, ctx.author)

            await ctx.bot.wait_for("reaction_add", check=pred)
        except asyncio.TimeoutError:
            await self._cleanup(all=True)
            return await ctx.send(
                self.parent._(
                    "Embed {} timed out.".format(
                        self.editor_data["edit_type"]["action"]
                    )
                )
            )

        await self._cleanup(comfirm=confirm, preview=preview)

        return pred.result

    async def _save(self, cancel=False, done=False):
        """
        Save an embed.
        """

        embed_data = self.original if cancel else self.embed_data

        posted_embed = self.msg.embeds[0]

        posted_embed.title = (
            embed_data["title"] if "title" in embed_data else EmptyEmbed
        )
        posted_embed.description = (
            embed_data["description"] if "description" in embed_data else EmptyEmbed
        )

        if self.editor_data["inline"] and done:
            strip_title = self.parent._(
                " :: {} Embed".format(
                    self.editor_data["edit_type"]["title"].capitalize()
                )
            )
            posted_embed.title = sub(strip_title, "", posted_embed.title)

            strip_description = self.parent._("\n{}").format(
                self.editor_data["supported_desc"]
            )
            posted_embed.description = sub(
                strip_description, "", posted_embed.description
            )

        posted_embed.url = embed_data["url"] if "url" in embed_data else None

        if "color" in embed_data and embed_data["color"] != "unset":
            posted_embed.color = embed_data["color"]

        if "color" in embed_data and embed_data["color"] == "unset":
            posted_embed.color = EmptyEmbed

        if "image" in embed_data:
            posted_embed.set_image(url=embed_data["image"])

        if "thumbnail" in embed_data:
            posted_embed.set_thumbnail(url=embed_data["thumbnail"])

        if "footer_text" in embed_data:
            show_footer = type(embed_data["footer_text"]) == str

            if "footer_icon" in embed_data and show_footer:
                posted_embed.set_footer(
                    text=embed_data["footer_text"], icon_url=embed_data["footer_icon"]
                )

            if "footer_icon" not in embed_data and show_footer:
                posted_embed.set_footer(text=embed_data["footer_text"])

            if not show_footer:
                posted_embed.set_footer(text=EmptyEmbed)

        await self.msg.edit(embed=posted_embed)

    async def _set_color(self, ctx: commands.Context):
        """
        Set the color for an embed.
        """

        prompt = self.parent._(
            "Color can be a hex color code, or any of the following presets:\n"
        )

        valid = get_valid_colors(self)

        valid_keys = valid.keys()
        valid_keys = [*valid_keys]

        valid_prompt = ", ".join(
            l + ",\n" * (n % 6 == 5) for n, l in enumerate(valid_keys)
        )
        valid_prompt = " " + valid_prompt.replace("\n, ", "\n ")

        prompt = prompt + valid_prompt

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}\n```\n{}\n```".format(
                        "Enter the color for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                        prompt,
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            color = the_response.content.lstrip("#")
            is_valid = False

            for valid_color, value in valid.items():
                if color == valid_color:
                    color = value.lstrip("#")
                    is_valid = True

            if len(color) == 3:
                color = color + color

            if len(color) == 6 and search(r"^(?:[0-9a-fA-F]{3}){1,2}$", color):
                is_valid = True

            if the_response.content not in ["cancel", "unset"] and not is_valid:
                await self._cleanup()
                self.editor_data["errors"].append(
                    await ctx.send(
                        self.parent._("Cowardly refusing to set an invalid color.")
                    )
                )
                process = False
                continue

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            if is_valid:
                self.embed_data["color"] = format_color(self, ctx, the_response.content)

            if the_response.content == "unset":
                self.embed_data["color"] = "unset"

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_description(self, ctx: commands.Context):
        """
        Set an embed description.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the description for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["description"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["description"] = EmptyEmbed

            if self.editor_data["inline"]:
                if the_response.content == "unset":
                    new_description = ""
                else:
                    new_description = self.embed_data["description"] + "\n"

                self.embed_data["description"] = self.parent._("{}{}").format(
                    new_description, self.editor_data["supported_desc"]
                )

                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_footer_text(self, ctx: commands.Context):
        """
        Set the footer text for an embed.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the footer text for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["footer_text"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["footer_text"] = EmptyEmbed

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_footer_icon(self, ctx: commands.Context):
        """
        Set the footer icon URL for an embed.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the footer icon URL for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            await self._cleanup()

            if the_response.content not in ["cancel", "unset"] and not valid_url(
                url=the_response.content, context="image"
            ):
                self.editor_data["errors"].append(
                    await ctx.send(
                        self.parent._("Cowardly refusing to set an invalid image URL.")
                    )
                )
                process = False
                continue

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["footer_icon"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["footer_icon"] = EmptyEmbed

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_image(self, ctx: commands.Context):
        """
        Set an embed image.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the image URL for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            await self._cleanup()

            if the_response.content not in ["cancel", "unset"] and not valid_url(
                url=the_response.content, context="image"
            ):
                self.editor_data["errors"].append(
                    await ctx.send(
                        self.parent._("Cowardly refusing to set an invalid image URL.")
                    )
                )
                process = False
                continue

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["image"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["image"] = ""

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_thumbnail(self, ctx: commands.Context):
        """
        Set an embed thumbnail.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the thumbnail URL for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            await self._cleanup()

            if the_response.content not in ["cancel", "unset"] and not valid_url(
                url=the_response.content, context="image"
            ):
                self.editor_data["errors"].append(
                    await ctx.send(
                        self.parent._("Cowardly refusing to set an invalid image URL.")
                    )
                )
                process = False
                continue

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["thumbnail"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["thumbnail"] = ""

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_title(self, ctx: commands.Context):
        """
        Set an embed title.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the title for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["title"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["title"] = EmptyEmbed

            if self.editor_data["inline"]:
                if the_response.content == "unset":
                    new_title = self.editor_data["cog_name"]
                else:
                    new_title = self.embed_data["title"]

                self.embed_data["title"] = self.parent._(
                    "{} :: {} Embed".format(
                        new_title, self.editor_data["edit_type"]["title"].capitalize()
                    )
                )

                await self._save()

            await self._cleanup()

            process = False
            continue

    async def _set_url(self, ctx: commands.Context):
        """
        Set an embed URL.
        """

        self.editor_data["prompts"].append(
            await ctx.send(
                self.parent._(
                    "{} {}".format(
                        "Enter the URL for the embed.",
                        "Entering `cancel` will cancel input, entering `unset` will clear the field.",
                    )
                )
            )
        )

        process = True

        while process:
            try:
                the_response = await self.parent.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30,
                )

                self.editor_data["responses"].append(the_response)
            except asyncio.TimeoutError:
                await self._cleanup(all=True)
                return await ctx.send(
                    self.parent._(
                        "Embed {} timed out.".format(
                            self.editor_data["edit_type"]["action"]
                        )
                    )
                )

            await self._cleanup()

            if the_response.content not in ["cancel", "unset"] and not valid_url(
                the_response.content
            ):
                self.editor_data["errors"].append(
                    await ctx.send(
                        self.parent._("Cowardly refusing to set an invalid URL.")
                    )
                )
                process = False
                continue

            if the_response.content == "cancel":
                await self._cleanup()
                process = False
                continue

            self.embed_data["url"] = the_response.content

            if the_response.content == "unset":
                self.embed_data["url"] = EmptyEmbed

            if self.editor_data["inline"]:
                await self._save()

            await self._cleanup()

            process = False
            continue


class WidgitEmbedException(Exception):
    """
    Exception handler for WidgetEmbed
    """
