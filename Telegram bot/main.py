from typing import Final

from openpyxl.writer.theme import theme_xml
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import sqlite3

#Global variables
CHOOSING = 1
name = ""
dict_names = {}
query = "Please enter the name of the student you would like to search."
def start():
    conn = sqlite3.connect("storage.db")



menu = "What would you like to do?:\n1. Add Incident\n2. Search student\n3. End"

TOKEN: Final = "BLANK"

BOT_USERNAME: Final = "@School_Manager_Test_Bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Need any help? Here is some info\n\n"
                                    f"This is a simple game I made about you.\n"
                                    f"All you need to do is complete all the mini gamesto unlock a mysterious "
                                    f"final reward.\n"
                                    f"Also you get points for typing panda, but the points literally do nothing\n\n"
                                    f"Originally, the points were actually supposed to do something\n"
                                    f"Then I realised I no time to finish, so Yay just finish 3 mini games to unlock"
                                    f"The final reward.\n"
                                    f"Have funnnnn! Best valentines gift ever.\n")
    msg = "Hello! " \
          "Pls enter your name so we can get started!"
    await update.message.reply_text(msg)
    return "startGame"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Here are some things you can say\n"
                                    f"Mini1: enters minigame 1\n"
                                    f"Mini2: enters minigame 2\n"
                                    f"Mini3: enters minigame 3\n"
                                    f"points: shows your points\n"
                                    f"panda: Get more points\n")


async def quit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation quit successfully!")
    return ConversationHandler.END


# Responses
async def GameStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("storage.db")
    text = update.message.text
    print(f"Select * from Store WHERE Name = '{text}'")
    with conn:
        info = conn.execute(f"Select * from Store WHERE Name = '{text}'")
        data = [i for i in info]

        if len(data) == 0:
            conn.execute(f"INSERT INTO Store (Name, Points, Mini1, Mini2, Mini3, Scale) "
                    f"Values ('{text}', 0, 0, 0, 0, 0)")
            info = conn.execute(f"Select * from Store WHERE Name = '{text}'")
            data = [i for i in info]
    context.user_data["points"] = data[0][1]
    context.user_data["name"] = text
    context.user_data["scale"] = data[0][5]
    context.user_data["mini1"] = data[0][2]
    context.user_data["mini2"] = data[0][3]
    context.user_data["mini3"] = data[0][4]
    msg = (f"Welcome {context.user_data["name"]}\n\n"
           f"You have {context.user_data["points"]} points.\n"
           f"They literally do nothing."
           f"Type panda to get more points!\n"
           f"Or type The name of the mini game to play!\n\n"
           )
    await update.message.reply_text(msg)

    await update.message.reply_text(menu(context))
    return "loop"


def menu(context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("storage.db")
    with conn:
        info = conn.execute(f"Select * from Store WHERE Name = '{context.user_data["name"]}'")
        data = [i for i in info]

    context.user_data["mini1"] = int(data[0][2])
    context.user_data["mini2"] = int(data[0][3])
    context.user_data["mini3"] = int(data[0][4])
    msg = (f"MINI GAME STATUS\n\n"
           f"Mini1 : {context.user_data["mini1"]}\n"
           f"Mini2 : {context.user_data["mini2"]}\n"
           f"Mini3 : {context.user_data["mini3"]}\n\n"
           f"0 is not done and 1 is done you fat. do /help if you dk what to do")
    if context.user_data["mini1"] and context.user_data["mini2"] and context.user_data["mini3"]:
        msg += ("\nWow you finished all the games! Now all you need to do is say the last 3 magical "
                "words to unlock the final reward! I wonder what those 3 words are that you always "
                "struggle to say?")
    return msg

async def loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("storage.db")
    text = update.message.text
    if text == "I love you" and context.user_data["mini1"] and context.user_data["mini2"] and context.user_data["mini3"]:
        msg = ("Wow, you finally made it, good job on finishing the stupid game I made!\n"
               "It is now 2:16am in the morning, and I still gotta test if this works. You really "
               "Make me always work so hard for you. But I always like to imagine you reading this message. "
               "And smiling to yourself. It always makes everything I do so much more worth it.\n\n"
               "So, its been about a 3ish months already, youre pretty old! Also for all I know, "
               "you could have a giant skill issue and finish this game in like 4 months. Who knows? "
               "But on a more serious note(which is very unlike me) Im super grateful for these 3 months"
               "that I had with you. I actually dont think Ive ever laughed so hard with anyone (The night"
               " I was walking with you to mcdonalds, I legit had one of the best times in my life.)\n\n"
               "So yeah, I said this a bunch of times already, but thank you for being my precious little fattie! "
               "I legit, havent had a day where I didnt think about you at all, more like I still cant stop thinking about "
               "you. \n\n"
               "So yes, if you would be ever so kind, please continue loving me! It blows my mind to pieces that someone"
               " (apart from family) would cry just cos I said my neck is itchy. Precious little fatties like you"
               " are the reasons why men fight wars. Knowing that you are safe and happy is all I need. \n\n"
               "A bit of a fat story, but that one time I heard about the light house incident, the guy that passed "
               "from natural causes. I was actually kinda freaking out. I knew the chance was super super low "
               "something bad even happened to you, but how would I know? OMG the relief when you texted me was insaneeeee.\n\n"
               "But lastly, HAPPY VALENTINES DAYYYYY, and cheers to many more valentines days to come!\n\n"
               "Your precious fattie\n"
               "Turtle")
        await update.message.reply_text(msg)
        return "loop"

    elif text == "panda":
        context.user_data["points"] += 1
        score = context.user_data["points"]
        with conn:
            conn.execute(f"UPDATE Store SET Points = {score} WHERE Name = '{context.user_data["name"]}'")
        await update.message.reply_text("+1")
        return "loop"
    elif text == "points":
        await update.message.reply_text(f"You have {context.user_data["points"]} points.")
        return "loop"
    elif text == "Mini1":
        msg = (f"Here is a simple one, lets see if you remember the nonsense I say\n\n"
           f"Which Upper case letter would make a super good house to stay in?\n"
           f"With multiple stories and even a roof? But I must have a floor.\n"
           f"So what letter is it?"
           )
        await update.message.reply_text(msg)
        return "Mini1"
    elif text == "Mini2":
        msg = (f"Now a bit more abitious, What is the exact distance I walked for my 72km army walk?\n\n"
               f"Hint: Might be found on a certain social media platform.")
        await update.message.reply_text(msg)
        return "Mini2"
    elif text == "Mini3":
        msg = ("I love you! Anyways your last game if you doing in order is....\n"
               "Remember the notes you gave me in the blue envelope?\n\n"
               "How many times did you say I love you in total?\n"
               "No hints you should know.")
        await update.message.reply_text(msg)
        return "Mini3"
    else:
        await update.message.reply_text("Skill issue you type wrong, pls check its the exact spelling\n"
                                        "i.e type exactly Mini1 for example.")
        return "loop"

def updatescore(text, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("storage.db")
    with conn:
        conn.execute(f"UPDATE Store SET {text} = 1 WHERE Name = '{context.user_data["name"]}'")

async def mini1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "E":
        msg = ("Yayyyyy you got it im so proud of you, you got more to go!,\n"
               "(Actually I got no idea you could have done it not in order).\n"
               "Continue with the other mini games by typing their names!")
        await update.message.reply_text(msg)

        updatescore("Mini1", context)
        await update.message.reply_text(menu(context))
        return "loop"
    elif text == "A":
        msg = ("No floor it aint good man, try again.")
        await update.message.reply_text(msg)
        return "Mini1"
    else:
        await update.message.reply_text("Nope try againnnn")
        return "Mini1"

async def mini2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "77.09":
        msg = ("Wahhhh youre a smartieeeeee! you got more to go!,\n"
               "(Actually I got no idea you could have done it not in order).\n"
               "Continue with the other mini games by typing their names!")
        await update.message.reply_text(msg)

        updatescore("Mini2", context)
        await update.message.reply_text(menu(context))
        return "loop"
    elif text == "90":
        msg = ("Thats for thailand, it may be another number you see.")
        await update.message.reply_text(msg)
        return "Mini2"
    elif text == "72":
        msg = ("Dont be lame lahhhh of course its not that easy.")
        await update.message.reply_text(msg)
        return "Mini2"
    else:
        await update.message.reply_text("Nope try againnnn. Please just write the number without the km.")
        return "Mini2"

async def mini3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text[0] == "-" and text[1:].isnumeric():
        msg = (f"Okay this means you owe me {text[1:]} I love yousss.")
        await update.message.reply_text(msg)
        return "Mini3"
    elif not text.isnumeric():
        msg = ("Omg you potato, you didnt even type a number.\n"
               "What in the world are you doing you fat.\n"
               "Btw Im writing this at 2:03am and I wanted to say I love youuuu.\n"
               "You are fat and mean the world to me, but Ill continue my speech in the final prize")
        await update.message.reply_text(msg)
        return "Mini3"
    elif int(text) < 2:
        msg = ("Thats way way way too low, why you even guess so low?")
        await update.message.reply_text(msg)
        return "Mini3"
    elif int(text) < 4:
        msg = ("Almost, just a little higher!")
        await update.message.reply_text(msg)
        return "Mini3"
    elif int(text) > 7:
        msg = ("Wah very high ahhh, aint right.")
        await update.message.reply_text(msg)
        return "Mini3"
    elif int(text) > 4:
        msg = ("A tad too high fattie")
        await update.message.reply_text(msg)
        return "Mini3"
    elif int(text) == 4:
        msg = ("WOWWWW you got it! Actually Its way less than I thought too. \n"
               "Now if you did in order, Hopefully the final message would appear!")
        await update.message.reply_text(msg)
        updatescore("Mini3", context)
        await update.message.reply_text(menu(context))
        return "loop"
    else:
        await update.message.reply_text("Nope try againnnn. Please just write the number without the km.")

        updatescore("Mini3", context)
        await update.message.reply_text(menu(context))
        return "Mini3"




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END





async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    start()
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            "startGame": [MessageHandler(filters.TEXT & ~filters.COMMAND, GameStart)],
            #"Intermediate": [MessageHandler(filters.TEXT & ~filters.COMMAND, intermediate)],
            "loop": [MessageHandler(filters.TEXT & ~filters.COMMAND, loop)],
            "Mini1": [MessageHandler(filters.TEXT & ~filters.COMMAND, mini1)],
            "Mini2": [MessageHandler(filters.TEXT & ~filters.COMMAND, mini2)],
            "Mini3": [MessageHandler(filters.TEXT & ~filters.COMMAND, mini3)]
        },
        fallbacks=[CommandHandler("quit", quit_command)],
    )
    app.add_handler(conv_handler)
    # app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    # app.add_handler(CommandHandler("quit", quit_command))

    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
