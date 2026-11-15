import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الآيدي الخاص بك على تليجرام
ADMIN_CHAT_ID = 6320201370

user_states = {}

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states.pop(user_id, None)
    user_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("💳 سحب الأرباح والحوالات المالية", callback_data="payouts_and_transfers")],
        [InlineKeyboardButton("💰 طرق الدفع وشحن الرصيد", callback_data="payment_methods")],
        [InlineKeyboardButton("🎮 شحن ألعاب وتطبيقات وبرامج", callback_data="services")],
        [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في Black Store للخدمات الرقمية! 🚀\n\n"
        "نحن نساعدك في تأمين خدماتك وتسهيل عمليات سحب وتحويل الأرباح بكل أمان وسرعة.\n\n"
        "اختر ما تحتاجه من القائمة أدناه:",
        reply_markup=reply_markup
    )

# معالجة الأزرار والأقسام
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data == "payouts_and_transfers":
        user_states.pop(user_id, None)
        text = (
            "💳 **قسم سحب الأرباح والحوالات المالية:**\n\n"
            "💵 **1. السحب من البرامج والأرباح الرقمية:**\n"
            "🔸 **USDT (شبكة TRC20):**\n"
            "`TH8onYYbwcybN2BoWB1c5MTju6Gxbff5ZV`\n\n"
            "🔸 **USDT (شبكة BEP20):**\n"
            "`0xf53a08352a1fac9e482b6054e45416e17e370e91`\n\n"
            "🛒 **حساب eBay / الأرباح:**\n"
            "• البريد المرتبط: `balckh86@gmail.com`\n"
            "⚠️ *إذا لم يعمل الإيميل، الرجاء مراجعة فريق الدعم.*\n\n"
            "──────────────────\n"
            "💸 **2. الحوالات المالية (تحديد طريقة الاستلام):**\n"
            "• يمكنك طلب استلام حوالتك عبر مراكز الصرافة أو عبر محافظ شام كاش / سيرياتيل كاش.\n"
            "⏱️ **مدة التنفيذ:** من ساعة إلى 24 ساعة.\n\n"
            "• اضغط على زر 'إرسال طلب حوالة' بالأسفل وأدخل البيانات المطلوبة."
        )
        keyboard = [
            [InlineKeyboardButton("📤 إرسال طلب حوالة", callback_data="start_transfer_order")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "payment_methods":
        user_states.pop(user_id, None)
        text = (
            "💰 **طرق الدفع المتاحة للشحن والتحويل:**\n"
            "• الحد الأدنى للشحن: 250 ليرة جديدة.\n\n"
            "🔸 **سيرياتيل كاش (Syriatel Cash):**\n"
            "رقم الحساب: `44179716`\n\n"
            "🔸 **شام كاش (Sham Cash):**\n"
            "معرف الحساب: `f5c166ff244f8806a68d446fc7d7d516`\n\n"
            "🔸 **USDT (TRC20):**\n"
            "`TH8onYYbwcybN2BoWB1c5MTju6Gxbff5ZV`\n\n"
            "🔸 **USDT (BEP20):**\n"
            "`0xf53a08352a1fac9e482b6054e45416e17e370e91`\n\n"
            "🛒 **eBay / PayPal:**\n"
            "• الإيميل المرتبط: `balckh86@gmail.com`\n"
            "⚠️ *إذا لم يعمل الإيميل، الرجاء مراجعة فريق الدعم.*"
        )
        keyboard = [
            [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "services":
        user_states.pop(user_id, None)
        text = (
            "🎮 **قسم شحن ألعاب وتطبيقات وبرامج:**\n"
            "• الحد الأدنى للطلب: 250 ليرة جديدة.\n"
            "⏱️ **مدة التنفيذ:** من دقيقة واحدة إلى 30 دقيقة.\n\n"
            "• شحن رصيد الألعاب والمنصات الشهيرة.\n"
            "• تفعيل واشتراكات التطبيقات والبرامج المدفوعة.\n\n"
            "👇 للطلب، اضغط على زر 'إرسال طلب سحب أو شحن'."
        )
        keyboard = [
            [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "start_order":
        user_states[user_id] = "waiting_for_item_details"
        text = (
            "📝 **خطوة 1 من 3: تفاصيل الطلب**\n"
            "⚠️ *الحد الأدنى للكمية أو الشحن هو 250 ليرة جديدة*\n"
            "⏱️ *وقت التنفيذ: من دقيقة إلى 30 دقيقة*\n\n"
            "🎮 أرسل الآن **اسم اللعبة أو البرنامج أو التطبيق** المراد شحنه مع **الكمية المطلوبة**:"
        )
        keyboard = [[InlineKeyboardButton("🔙 إلغاء والعودة", callback_data="back")]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "start_transfer_order":
        user_states[user_id] = "waiting_for_transfer_location"
        text = (
            "💸 **خطوة 1 من 4: تحديد طريقة أو مركز الاستلام**\n"
            "⏱️ *وقت تنفيذ الحوالة: من ساعة إلى 24 ساعة*\n\n"
            "🏢 أرسل في رسالة نصية **مركز الصرافة** (مثل الفاضل، الهرم) أو اكتب **شام كاش / سيرياتيل كاش**:"
        )
        keyboard = [[InlineKeyboardButton("🔙 إلغاء والعودة", callback_data="back")]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "back":
        user_states.pop(user_id, None)
        keyboard = [
            [InlineKeyboardButton("💳 سحب الأرباح والحوالات المالية", callback_data="payouts_and_transfers")],
            [InlineKeyboardButton("💰 طرق الدفع وشحن الرصيد", callback_data="payment_methods")],
            [InlineKeyboardButton("🎮 شحن ألعاب وتطبيقات وبرامج", callback_data="services")],
            [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="القائمة الرئيسية لمتجر Black Store 🚀\nاختر ما تحتاجه:",
            reply_markup=reply_markup
        )

# استقبال رسائل الزبائن مع معالجة دقيقة للأخطاء والتوجيه الصحيح
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    
    if user_id in user_states:
        current_state = user_states[user_id]
        
        # 1. حالة انتظار تفاصيل الطلب (ألعاب/تطبيقات/شحن)
        if current_state == "waiting_for_item_details":
            if update.message.text:
                item_details = update.message.text
                context.user_data['item_details'] = item_details
                user_states[user_id] = "waiting_for_address"
                
                await update.message.reply_text(
                    f"✅ تم تسجيل طلبك:\n`{item_details}`\n\n"
                    "💰 **خطوة 2 من 3: التحويل وإرسال معلومات الحساب**\n"
                    "⏱️ *وقت التنفيذ: من دقيقة إلى 30 دقيقة*\n"
                    "قم بتحويل المبلغ (الحد الأدنى 250 ليرة جديدة) عبر إحدى طرق الدفع التالية:\n\n"
                    "🔸 **سيرياتيل كاش:** `44179716`\n"
                    "🔸 **شام كاش:** `f5c166ff244f8806a68d446fc7d7d516`\n"
                    "🔸 **USDT (TRC20):**\n`TH8onYYbwcybN2BoWB1c5MTju6Gxbff5ZV`\n"
                    "🔸 **USDT (BEP20):**\n`0xf53a08352a1fac9e482b6054e45416e17e370e91`\n"
                    "🛒 **eBay / PayPal:** `balckh86@gmail.com`\n"
                    "⚠️ *إذا لم يعمل الإيميل، الرجاء مراجعة فريق الدعم.*\n\n"
                    "🔗 **الآن، أرسل في رسالة نصية:** رابط محفظتك أو معرف الحساب المطلوب إرسال الخدمة أو التحويل إليه:",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** أنت في خطوة كتابة تفاصيل الطلب.\n"
                    "يرجى إرسال **اسم اللعبة أو التطبيق والكمية كنص كتابي**، أو إرسال /start للعودة للقائمة الرئيسية."
                )
            
        # 2. حالة انتظار عنوان المحفظة أو الحساب
        elif current_state == "waiting_for_address":
            if update.message.text:
                wallet_address = update.message.text
                context.user_data['wallet_address'] = wallet_address
                user_states[user_id] = "waiting_for_photo"
                
                await update.message.reply_text(
                    f"✅ تم حفظ العنوان/الحساب:\n`{wallet_address}`\n\n"
                    "📷 **خطوة 3 من 3: أرسل صورة الإيصال**\n"
                    "الآن قم بإرسال صورة إيصال التحويل (لقطة شاشة) لإتمام العملية:",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** أنت في خطوة إرسال عنوان المحفظة أو الحساب.\n"
                    "يرجى إرسال العنوان المطلوب على شكل **نص**، أو إرسال /start للعودة."
                )
            
        # 3. حالة انتظار صورة الإيصال للطلب العادي
        elif current_state == "waiting_for_photo":
            if update.message.photo:
                item_details = context.user_data.get('item_details', 'غير متوفر')
                wallet_address = context.user_data.get('wallet_address', 'غير متوفر')
                
                photo_file = await update.message.photo[-1].get_file()
                file_name = f"order_{user_id}.jpg"
                await photo_file.download_to_drive(file_name)
                
                await update.message.reply_text(
                    "✅ **تم تقديم الطلب بنجاح!**\n"
                    "⏱️ *سيتم تنفيذ طلبك خلال (من دقيقة إلى 30 دقيقة)*.\n"
                    "تم تسجيل طلبك وصورة الإيصال وإرسالها للإدارة للمعالجة."
                )
                
                admin_message = (
                    f"🚨 **طلب جديد متكامل وصل!**\n\n"
                    f"👤 **اسم الزبون:** {user.first_name}\n"
                    f"🔗 **المعرف:** @{user.username or 'بدون معرف'}\n"
                    f"🆔 **رقم الآيدي:** `{user_id}`\n\n"
                    f"🎮 **الطلب (البرنامج/اللعبة + الكمية):**\n`{item_details}`\n\n"
                    f"📌 **الحساب / العنوان المطلوب التحويل إليه:**\n`{wallet_address}`"
                )
                
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message, parse_mode="Markdown")
                
                with open(file_name, 'rb') as photo_to_send:
                    await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_to_send, caption=f"إيصال الزبون: {user.first_name}")
                
                user_states.pop(user_id, None)
                context.user_data.pop('item_details', None)
                context.user_data.pop('wallet_address', None)
                
                keyboard = [
                    [InlineKeyboardButton("💳 سحب الأرباح والحوالات المالية", callback_data="payouts_and_transfers")],
                    [InlineKeyboardButton("💰 طرق الدفع وشحن الرصيد", callback_data="payment_methods")],
                    [InlineKeyboardButton("🎮 شحن ألعاب وتطبيقات وبرامج", callback_data="services")],
                    [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "اختر خدمة أخرى من القائمة أدناه:",
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** أنت في الخطوة الأخيرة لتأكيد الطلب.\n"
                    "يرجى إرسال **صورة إيصال التحويل (لقطة شاشة)** حصراً، ولا تقم بإرسال نصوص في هذه الخطوة."
                )

        # 4. مسار الحوالات المالية: الخطوة 1 (مركز الحوالة أو طريقة الاستلام)
        elif current_state == "waiting_for_transfer_location":
            if update.message.text:
                context.user_data['transfer_location'] = update.message.text
                user_states[user_id] = "waiting_for_wallet_number"
                
                await update.message.reply_text(
                    "💳 **خطوة 2 من 4: رقم الحساب أو المحفظة**\n\n"
                    "أرسل **رقم حساب شام كاش** أو **رقم سيرياتيل كاش** الخاص بك (أو اكتب 'لايوجد' إذا كانت حوالة لمركز صرافة):",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** يرجى كتابة مركز الصرافة أو طريقة الاستلام كنص كتابي."
                )

        # 5. مسار الحوالات المالية: الخطوة 2 (رقم حساب الشام كاش أو سيرياتيل كاش)
        elif current_state == "waiting_for_wallet_number":
            if update.message.text:
                context.user_data['transfer_wallet'] = update.message.text
                user_states[user_id] = "waiting_for_transfer_details"
                
                await update.message.reply_text(
                    "👤 **خطوة 3 من 4: البيانات الشخصية**\n\n"
                    "يرجى إرسال **الاسم الثلاثي، مكان الإقامة، ورقم الهاتف** في رسالة واحدة:",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** يرجى إرسال رقم الحساب أو المحفظة كنص كتابي."
                )

        # 6. مسار الحوالات المالية: الخطوة 3 (البيانات الشخصية)
        elif current_state == "waiting_for_transfer_details":
            if update.message.text:
                context.user_data['transfer_details'] = update.message.text
                user_states[user_id] = "waiting_for_transfer_photo"
                
                await update.message.reply_text(
                    "📷 **خطوة 4 من 4: أرسل صورة الإيصال**\n\n"
                    "الآن قم بإرسال صورة إيصال التحويل (لقطة شاشة) لإتمام طلب الحوالة:",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** يرجى إرسال البيانات الشخصية (الاسم الثلاثي، مكان الإقامة، ورقم الهاتف) كنص كتابي."
                )

        # 7. مسار الحوالات المالية: الخطوة 4 (صورة الإيصال والتأكيد)
        elif current_state == "waiting_for_transfer_photo":
            if update.message.photo:
                transfer_location = context.user_data.get('transfer_location', 'غير متوفر')
                transfer_wallet = context.user_data.get('transfer_wallet', 'غير متوفر')
                transfer_details = context.user_data.get('transfer_details', 'غير متوفر')
                
                photo_file = await update.message.photo[-1].get_file()
                file_name = f"transfer_{user_id}.jpg"
                await photo_file.download_to_drive(file_name)
                
                await update.message.reply_text(
                    "✅ **تم تقديم طلب الحوالة بنجاح!**\n"
                    "⏱️ *سيتم تنفيذ الحوالة خلال (من ساعة إلى 24 ساعة)*.\n"
                    "تم إرسال تفاصيل الاستلام والبيانات وصورة الإيصال للإدارة للتنفيذ."
                )
                
                admin_message = (
                    f"🚨 **طلب حوالة مالية جديدة وصل!**\n\n"
                    f"👤 **اسم حساب التليجرام:** {user.first_name}\n"
                    f"🔗 **المعرف:** @{user.username or 'بدون معرف'}\n"
                    f"🆔 **رقم الآيدي:** `{user_id}`\n\n"
                    f"🏢 **طريقة / مركز الاستلام:**\n`{transfer_location}`\n\n"
                    f"💳 **رقم حساب شام كاش / سيرياتيل كاش:**\n`{transfer_wallet}`\n\n"
                    f"📋 **البيانات الشخصية (الاسم، الإقامة، الهاتف):**\n`{transfer_details}`"
                )
                
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message, parse_mode="Markdown")
                
                with open(file_name, 'rb') as photo_to_send:
                    await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_to_send, caption=f"إيصال حوالة من: {user.first_name}")
                
                user_states.pop(user_id, None)
                context.user_data.pop('transfer_location', None)
                context.user_data.pop('transfer_wallet', None)
                context.user_data.pop('transfer_details', None)
                
                keyboard = [
                    [InlineKeyboardButton("💳 سحب الأرباح والحوالات المالية", callback_data="payouts_and_transfers")],
                    [InlineKeyboardButton("💰 طرق الدفع وشحن الرصيد", callback_data="payment_methods")],
                    [InlineKeyboardButton("🎮 شحن ألعاب وتطبيقات وبرامج", callback_data="services")],
                    [InlineKeyboardButton("📤 إرسال طلب سحب أو شحن", callback_data="start_order")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "اختر خدمة أخرى من القائمة أدناه:",
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    "⚠️ **خطأ في الإدخال:** أنت في خطوة إرسال إيصال الحوالة المالية.\n"
                    "يرجى إرسال **صورة** الإيصال حصراً لإتمام الطلب، ولا تقم بإرسال نصوص."
                )
    else:
        await update.message.reply_text(
            "⚠️ **تنبيه:** لم تقم باختيار أي عملية نشطة حالياً.\n"
            "يرجى استخدام الأزرار التفاعلية أو إرسال الأمر /start للعودة إلى القائمة الرئيسية."
        )

if __name__ == '__main__':
    TOKEN = "9092595881:AAEMhrr9QxJZ22XUOIrOAEXERddWajWa-DY"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_message))
    
    print("Black Store Bot is running...")
    app.run_polling()