import logging
import os

from discord_webhook import DiscordEmbed, DiscordWebhook

class Discord:
    def __init__(
        self, webhook_url, role_ids, user_ids, platform, thumb_url, embed_color,
        embed_title=None, embed_footer=None, embed_description=None
    ):
        self.logger = logging.getLogger(__name__)
        self.platform = platform
        self.webhook_url = webhook_url
        self.role_ids = role_ids
        self.user_ids = user_ids
        self.thumb_url = thumb_url
        self.embed_color = embed_color
        self.embed_title = embed_title or f"{self.platform} Game Update Alert!"
        self.embed_footer = embed_footer or "Custom Fork Notifier"
        self.embed_description = embed_description or "The following games have updates:"

    def get_local_asset(self):
        asset_map = {
            "steam": "assets/steam.png",
            "gog": "assets/gog.png",
            "epicgames": "assets/epicgames.png",
            "msstore": "assets/msstore.png",
        }
        asset_path = asset_map.get(self.platform.lower())
        if asset_path and os.path.exists(asset_path):
            return f"file://{os.path.abspath(asset_path)}"
        return self.thumb_url

    def create_embed_message(self, updated_apps, timestamp):
        _embed = DiscordEmbed(
            title=self.embed_title,
            description=self.embed_description,
            color=self.embed_color,
        )
        thumb = self.get_local_asset()
        if thumb:
            _embed.set_thumbnail(url=thumb)

        for app in updated_apps:
            details = f"ID: `{app.id}`"
            update_time = getattr(app, "last_updated", None) or timestamp
            details += f"\nDetected: `{update_time.strftime('%Y-%m-%d %H:%M:%S')}`"
            _embed.add_embed_field(name=app.name, value=details, inline=False)

        _embed.set_footer(text=self.embed_footer)
        _embed.set_timestamp()
        return _embed

    def fire(self, updated_apps, timestamp):
        self.logger.info("Prepare webhook")
        _webhook = DiscordWebhook(url=self.webhook_url)

        mentions = []
        for rid in self.role_ids:
            if rid:
                mentions.append(f"<@&{rid}>")
        for uid in self.user_ids:
            if uid:
                mentions.append(f"<@{uid}>")
        content = " ".join(mentions) if mentions else None
        if content:
            _webhook.content = content

        self.logger.info("Construct embed message")
        _embed = self.create_embed_message(updated_apps, timestamp)

        self.logger.info("Post embed message")
        _webhook.add_embed(_embed)
        _webhook.execute()
