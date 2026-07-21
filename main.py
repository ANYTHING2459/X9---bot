import os, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
TOKEN=os.environ.get("TOKEN")
SERPAPI_KEY=os.environ.get("SERPAPI_KEY")
def upload_smart(path):
    try:
        with open(path,"rb") as f:
            r=requests.post("https://catbox.moe/user/api.php",data={"reqtype":"fileupload"},files={"fileToUpload":f},timeout=15)
            if "http" in r.text: return r.text.strip()
    except: pass
    try:
        with open(path,"rb") as f:
            r=requests.post("https://0x0.st",files={"file":f},timeout=15)
            if "http" in r.text: return r.text.strip()
    except: pass
    raise Exception("فشل الرفع")
async def start(update,context): await update.message.reply_text("بوت X9 جاهز ✅\nرسل صورة + وصف معاها")
async def on_photo(update,context):
    cap=update.message.caption or ""
    await update.message.reply_text(f"⏳ بفتش: {cap}...")
    file=await context.bot.get_file(update.message.photo[-1].file_id)
    await file.download_to_drive("/tmp/img.jpg")
    try:
        img_url=upload_smart("/tmp/img.jpg")
        data=requests.get("https://serpapi.com/search",params={"engine":"google_lens","url":img_url,"api_key":SERPAPI_KEY},timeout=30).json()
        c=0
        for item in data.get("visual_matches",[])[:10]:
            try:
                await context.bot.send_photo(chat_id=update.effective_chat.id,photo=item.get("thumbnail"),caption=f"✅ {item.get('link')}")
                c+=1
                if c>=5: break
            except: pass
        if c==0: await update.message.reply_text("ما لقيت مطابق")
    except Exception as e: await update.message.reply_text(f"خطأ: {e}")
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.PHOTO,on_photo))
app.run_polling()
