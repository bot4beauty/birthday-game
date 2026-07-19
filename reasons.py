import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import PARSE_MD, REASON_VIEW
from helpers import (
    safe_edit_text, safe_edit_caption, safe_send_photo,
    create_single_button, edit_navigation_message
)
from animations import animation

# ==============================
# REASON DATA - PLACEHOLDERS
# ==============================

REASONS_DATA = [
    {"number": i, "image": f"reason_{i}.jpg", 
     "text": f"REASON {i} TEXT - Replace this with your beautiful reason"}
    for i in range(1, 23)
]

# ==============================
# REASONS HANDLERS
# ==============================

async def handle_continue_to_reasons(update, context):
    """Chapter 4: 22 Reasons - Optimized"""
    query = update.callback_query
    await query.answer()
    
    await edit_navigation_message(
        update, context,
        "💕 *Opening the Love Book...* 💕\n\n_Every reason is a piece of my heart..._ ❤️"
    )
    
    context.user_data['completed_reasons'] = []
    context.user_data['current_reason'] = 0
    
    introduction = (
        "🌸 *On your 22nd birthday...* 🌸\n\n"
        "There are countless reasons why I love you.\n\n"
        "But today I want to share just 22 of them.\n\n"
        "✨ Each one holds a little piece of my heart.\n\n"
        "_Take your time..._\n"
        "_Read them one by one._ 💕"
    )
    
    await query.message.reply_text(
        introduction,
        parse_mode=PARSE_MD,
        reply_markup=create_single_button("📖 Begin Reading", "reasons_begin")
    )

async def handle_reasons_begin(update, context):
    """Begin the 22 Reasons journey - Optimized"""
    query = update.callback_query
    await query.answer()
    
    await safe_edit_text(
        query.message,
        "✨ *Opening the pages of my heart...* ✨\n\n_Each reason is a precious memory..._ ❤️",
        PARSE_MD
    )
    
    await asyncio.sleep(0.3)
    await show_reason_list(update, context, query)

async def show_reason_list(update, context, query):
    """Show the list of reasons - Optimized"""
    completed = context.user_data.get('completed_reasons', [])
    total_reasons = len(REASONS_DATA)
    
    # Build reason list (optimized)
    reason_lines = []
    next_num = len(completed) + 1
    
    for i, reason in enumerate(REASONS_DATA, 1):
        if i in completed:
            reason_lines.append(f"✅ *Reason {i}*")
        elif i == next_num:
            reason_lines.append(f"❤️ *Reason {i}*")
        else:
            reason_lines.append(f"□ Reason {i}")
    
    reason_list = "\n".join(reason_lines)
    progress_hearts = "❤️" * len(completed) + "□" * (total_reasons - len(completed))
    
    if len(completed) == total_reasons:
        await show_final_reason_message(update, context, query)
        return
    
    keyboard = create_single_button(
        f"❤️ Reason {next_num}",
        f"reason_view_{next_num}"
    )
    
    message_text = (
        f"📖 *22 Reasons Why I Love You*\n\n"
        f"{reason_list}\n\n"
        f"✨ *Progress:* {len(completed)} / {total_reasons}\n"
        f"{progress_hearts}\n\n"
        f"_Touch the next reason to continue..._ 💕"
    )
    
    await query.message.reply_text(message_text, parse_mode=PARSE_MD, reply_markup=keyboard)

async def handle_reason_view(update, context):
    """Handle viewing a specific reason - Optimized"""
    query = update.callback_query
    await query.answer()
    
    reason_number = int(query.data.split('_')[2])
    completed = context.user_data.get('completed_reasons', [])
    
    if reason_number in completed:
        await query.answer("You've already read this reason! 💕")
        return
    
    next_expected = len(completed) + 1
    if reason_number != next_expected:
        await query.answer("Please read the reasons in order! 💕")
        return
    
    reason_data = REASONS_DATA[reason_number - 1]
    await show_reason_detail(update, context, query, reason_data)

async def show_reason_detail(update, context, query, reason_data):
    """Show a single reason - Optimized"""
    await safe_edit_text(
        query.message,
        f"💕 *Reason {reason_data['number']}* 💕\n\n_Opening..._ ✨",
        PARSE_MD
    )
    
    await asyncio.sleep(0.3)
    
    caption = f"❤️ *Reason {reason_data['number']}* ❤️\n\n_{reason_data['text']}_"
    keyboard = create_single_button(
        "✨ Continue",
        f"reason_complete_{reason_data['number']}"
    )
    
    try:
        await query.message.reply_photo(
            photo=open(reason_data['image'], "rb"),
            caption=caption,
            parse_mode=PARSE_MD,
            reply_markup=keyboard
        )
    except Exception:
        await query.message.reply_text(
            f"{caption}\n\n📷 *Image placeholder:* {reason_data['image']}",
            parse_mode=PARSE_MD,
            reply_markup=keyboard
        )

async def handle_reason_complete(update, context):
    """Mark reason as completed - Optimized"""
    query = update.callback_query
    await query.answer()
    
    reason_number = int(query.data.split('_')[2])
    completed = context.user_data.get('completed_reasons', [])
    
    if reason_number not in completed:
        completed.append(reason_number)
        context.user_data['completed_reasons'] = completed
    
    await safe_edit_caption(
        query.message,
        f"✅ *Reason {reason_number}* ✅\n\n_Completed with love..._ 💕",
        PARSE_MD
    )
    
    await asyncio.sleep(0.3)
    
    if len(completed) == len(REASONS_DATA):
        await show_final_reason_message(update, context, query)
    else:
        await show_reason_list(update, context, query)

async def show_final_reason_message(update, context, query):
    """Show the special final message - Optimized"""
    final_message = (
        "✨ *You've reached the final reason...* ✨\n\n"
        "_..._ 💕\n\n"
        "❤️ *The truth is...* ❤️\n\n"
        "_..._ 💕"
    )
    
    await query.message.reply_text(final_message, parse_mode=PARSE_MD)
    await asyncio.sleep(1.5)
    
    closing_message = (
        "I could never stop at 22.\n\n"
        "✨ Every single day,\n"
        "you give me another reason to love you.\n\n"
        "💕 So this isn't the end of the list.\n\n"
        "🌸 It's simply the beginning of a lifetime of new reasons.\n\n"
        "🎂 Happy 22nd Birthday, my love.\n\n"
        "❤️ *Thank you for reading every page of my heart.* ❤️"
    )
    
    await query.message.reply_text(closing_message, parse_mode=PARSE_MD)
    await asyncio.sleep(1)
    
    await animation.animate_sparkle(update)
    
    context.user_data['completed_reasons'] = []
    context.user_data['current_reason'] = 0
    
    await query.message.reply_text(
        "💫 *You've unlocked the final chapter...* 💫\n\n"
        "_The best surprise is waiting for you..._ ❤️",
        reply_markup=create_single_button("🎁 Continue to Final Surprise", "continue_to_finale"),
        parse_mode=PARSE_MD
      )
