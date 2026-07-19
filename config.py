import os
from datetime import datetime

# ==============================
# BOT CONFIGURATION
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GAME_URL = "https://birthday2game.netlify.app"

ALLOWED_USERS = {
    5246510881,
    8812025199,
}

RELATIONSHIP_START = datetime(2024, 1, 16)

# ==============================
# CONVERSATION STATES
# ==============================

SONG_ANSWER, QUIZ_ANSWER, REASON_VIEW = range(3)

# ==============================
# REUSABLE CONSTANTS
# ==============================

PARSE_MD = "Markdown"
PARSE_HTML = "HTML"

# Button texts
BTN_TEXTS = {
    "our_memories": "❤️ Our Memories",
    "our_song": "🎵 Our Song",
    "one_last_wish": "💭 One Last Wish",
    "22_reasons": "💕 22 Reasons",
    "final_surprise": "🎁 Final Surprise",
    "birthday_game": "🎈 Birthday Game",
    "return_home": "❤️ Return to Telegram"
}

# File paths
FILES = {
    "birthday_video": "birthday.mp4",
    "our_song": "our_song.mp3",
    "singing_clip": "singing_clip.mp3",
    "wish_image": "wish_image.jpg",
    "romantic_image": "romantic_moment.jpg",
}

# ==============================
# SPEED CONFIGURATION (Internal)
# ==============================

# These are used internally for performance optimization
# but don't change visible behavior
ANIMATION_SPEED = 0.3  # Multiplier for internal delays (0.3 = faster)
