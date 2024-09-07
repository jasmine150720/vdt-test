import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_USER = os.getenv('JENKINS_USER')
JENKINS_API_TOKEN = os.getenv('JENKINS_API_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send /pipelines to get the list of Jenkins pipelines.')

async def get_pipelines(update: Update, context: CallbackContext) -> None:
    
    response = requests.get(f"{JENKINS_URL}/api/json?tree=jobs[name]", auth=(JENKINS_USER, JENKINS_API_TOKEN))
    jobs = response.json().get('jobs', [])
    job_names = "\n".join(job['name'] for job in jobs)
    
    if job_names:
        await update.message.reply_text(f"Here are the pipelines:\n{job_names}")
    else:
        await update.message.reply_text("No pipelines found.")

def main() -> None:
    dispatcher = ApplicationBuilder().token(BOT_TOKEN).build()
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pipelines", get_pipelines))

    dispatcher.run_polling()

if __name__ == '__main__':
    main()
