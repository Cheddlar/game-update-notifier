import os
from datetime import datetime
from dotenv import load_dotenv
from modules.discord import Discord
from modules.models import App

def main():
    load_dotenv()

    # Dummy data for testing
    updated_apps = [
        App(id="123456", name="Test Game 1"),
        App(id="654321", name="Test Game 2"),
        App(id="111111", name="Test Game 3"),
    ]
    timestamp = datetime.now()

    # Example IDs for testing
    role_ids = ["123456789012345678"]
    user_ids = ["987654321098765432"]

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    notifier = Discord(
        webhook_url=webhook_url,
        role_ids=role_ids,
        user_ids=user_ids,
        platform="Steam",
        thumb_url="https://github.com/kurokobo/game-update-notifier/raw/main/assets/steam.png",
        embed_color="1e90ff",
    )

    embed = notifier.create_embed_message(updated_apps, timestamp)
    print("Embed attributes:", embed.__dict__)

    notifier.fire(updated_apps, timestamp)

if __name__ == "__main__":
    main()