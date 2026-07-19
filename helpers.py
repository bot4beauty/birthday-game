import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import PARSE_MD, BTN_TEXTS

# ==============================
# FILE CACHE
# ==============================

_file_cache = {}

def get_cached_file(file_path, mode="rb"):
    """Cache file contents for faster access"""
    if file_path not in _file_cache:
        try:
            with open(file_path, mode) as f:
                _file_cache[file_path] = f.read()
        except Exception:
            return None
    return _file_cache[file_path]

def clear_file_cache():
    """Clear the file cache"""
    _file_cache.clear()

# ==============================
# SAFE TELEGRAM OPERATIONS
# ==============================

async def safe_edit_text(message, text, parse_mode=PARSE_MD, **kwargs):
    """Safely edit message text"""
    try:
        return await message.edit_text(text, parse_mode=parse_mode, **kwargs)
    except Exception:
        return None

async def safe_edit_caption(message, caption, parse_mode=PARSE_MD, **kwargs):
    """Safely edit message caption"""
    try:
        return await message.edit_caption(caption=caption, parse_mode=parse_mode, **kwargs)
    except Exception:
        return None

async def safe_delete(message):
    """Safely delete a message"""
    try:
        await message.delete()
        return True
    except Exception:
        return False

async def safe_send_photo(context, chat_id, photo, caption="", parse_mode=PARSE_MD, **kwargs):
    """Safely send a photo with caching"""
    try:
        if isinstance(photo, str):
            # Try to use cached file
            cached = get_cached_file(photo)
            if cached:
                from io import BytesIO
                photo = BytesIO(cached)
        return await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            **kwargs
        )
    except Exception:
        return None

async def safe_send_audio(context, chat_id, audio, title="", **kwargs):
    """Safely send audio with caching"""
    try:
        if isinstance(audio, str):
            cached = get_cached_file(audio)
            if cached:
                from io import BytesIO
                audio = BytesIO(cached)
        return await context.bot.send_audio(
            chat_id=chat_id,
            audio=audio,
            title=title,
            **kwargs
        )
    except Exception:
        return None

# ==============================
# KEYBOARD HELPERS
# ==============================

def create_keyboard(buttons, row_width=1):
    """Create an inline keyboard from button list"""
    keyboard = []
    for i in range(0, len(buttons), row_width):
        row = buttons[i:i+row_width]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def create_single_button(text, callback_data):
    """Create a single button keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=callback_data)]
    ])

def get_button_text(chapter_name):
    """Get button text for a chapter"""
    return BTN_TEXTS.get(chapter_name, "➡ Continue")

# ==============================
# NAVIGATION HELPERS
# ==============================

async def edit_navigation_message(update, context, new_text, parse_mode=PARSE_MD):
    """Edit the current navigation message to remove buttons"""
    query = update.callback_query
    if query and query.message:
        return await safe_edit_text(query.message, new_text, parse_mode)
    return False

async def send_chapter_navigation(update, context, chapter_name, callback_data, chat_id=None):
    """Send themed navigation button for the next chapter"""
    button_text = get_button_text(chapter_name)
    keyboard = create_single_button(button_text, callback_data)
    
    message_text = f"💫 *Ready for the next chapter?* 💫\n\n_{button_text}_"
    
    if chat_id:
        return await context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=keyboard,
            parse_mode=PARSE_MD
        )
    else:
        target = update.callback_query or update.message
        if target:
            return await target.reply_text(
                message_text,
                reply_markup=keyboard,
                parse_mode=PARSE_MD
            )
    return None

# ==============================
# CALCULATION HELPERS
# ==============================

def calculate_journey(relationship_start):
    """Calculate journey duration - optimized"""
    from datetime import datetime, timedelta
    now = datetime.now()
    
    total_days = (now - relationship_start).days
    total_hours = int((now - relationship_start).total_seconds() // 3600)
    total_minutes = int((now - relationship_start).total_seconds() // 60)
    total_seconds = int((now - relationship_start).total_seconds())
    
    years = now.year - relationship_start.year
    months = now.month - relationship_start.month
    days = now.day - relationship_start.day
    
    if days < 0:
        months -= 1
        previous_month = now.replace(day=1) - timedelta(days=1)
        days += previous_month.day
    
    if months < 0:
        years -= 1
        months += 12
    
    return years, months, days, total_days, total_hours, total_minutes, total_seconds
