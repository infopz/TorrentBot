import pzgram
import rss
import db
import transmission

from config import bot_key, owner_id

bot = pzgram.Bot(bot_key)
ownerId = owner_id


def torrent_command(chat):
    torrent = transmission.get_torrent_status()
    text = ""
    for t in torrent:
        if t["error"]:
            text += "‼️ "
        if t["status"] == "Downloading":
            text += "*Name*: " + t["name"][:30] + "\n *Status*: ⏬ *" + t["perc"] \
                    + "*\n *DownSpeed*: " + t["dws"] + "\n *ETA*: " + t["eta"] + "\n\n"
        elif t["status"] == "Seeding":
            text += "*Name*: " + t["name"][:30] + "\n *Status*: ⏫ " + t["ups"] + "\n\n"
        elif t["status"] == "Up & Down":
            text += "*Name*: " + t["name"][:30] + "\n *Status*: ⏬⏫ *" + t["perc"] \
                    + "*\n *DS:* " + t["dws"] + "  *US:*" + t["ups"] + "\n *ETA*: " + t["eta"] + "\n\n"
        else:
            text += "*Name*: " + t["name"][:30] + "\n *Status*: " + t["status"] + " " + t["perc"] + "\n\n"
    chat.send(text, parse_mode="markdown")


def add_command(chat):
    chat.send("Inviami la pagina o il magnet da aggiungere")
    bot.set_next(chat, add_receive)


def add_receive(chat, message):
    link = message.text
    title, magnet, size = rss.analize_page(link)
    num = db.write_magnet(title, magnet)
    keyboard = [[pzgram.create_button("✅ Scarica", data="num_" + str(num)),
                 pzgram.create_button("❌ Cancella", data="del_2")]]
    keyboard = pzgram.create_inline(keyboard)
    chat.send("Confermi di voler aggiungere: \n*" + title + "*\n Peso: *" + size + "*",
              parse_mode="markdown", reply_markup=keyboard)


def check_new():
    feed = rss.check_rss()
    torrent = rss.analyze_feed(feed)
    if len(torrent):
        for t in torrent:
            s = t["size"].split()
            if s[1] == "MB":
                continue
            text = "Name: " + t["title"] + "\nSize: " + t["size"]
            keyboard = [[pzgram.create_button("✅ Scarica", data="num_" + str(t["number"])),
                         pzgram.create_button("❌ Cancella", data="del")]]
            keyboard = pzgram.create_inline(keyboard)
            pzgram.Chat(bot, ownerId).send(text, reply_markup=keyboard)


def check_torrent():
    torrents = transmission.get_torrent_status()
    for t in torrents:
        completed = 1 if t["perc"] == "100%" else 0
        d = db.get_torrent(t["name"])
        if d is None:
            db.add_torrent(t["name"], completed)
            if completed:
                pzgram.Chat(bot, ownerId).send("💯 Il download di *\n" + t["name"] + "\n* e' stato completato",
                                               parse_mode="markdown")

        elif completed and d[1] == 0:
            db.torrent_completed(t['name'])
            pzgram.Chat(bot, ownerId).send("💯 Il download di *\n" + t["name"] + "\n* e' stato completato",
                                           parse_mode="markdown")


def call_back(query, data):
    if data.startswith("num_"):
        num = int(data.split("_")[1])
        magnet = db.check_magnet(num)
        if magnet is not None and transmission.add_torrent(magnet):
            name = db.get_magnet(num)[1][:30]
            query.message.edit("*"+name + "* aggiunto ai download", parse_mode="markdown")
            query.reply("Torrent messo in Download")
        else:
            query.reply("Errore con il Torrent")
    elif data == "del":
        query.message.delete()
    elif data == "del_2":
        query.message.edit_reply_markup(None)


def check_user(sender):
    if sender.id != ownerId:
        return True


def process_message(chat, message):
    if message.text.startswith("https://ilcorsaronero.unblocker.cc/tor/"):
        add_receive(chat, message)


bot.callBackFunc = call_back
bot.processAll = check_user
bot.processMessage = process_message
bot.set_commands({"torrent": torrent_command, "add": add_command})
bot.set_timers({3600: check_new, 900: check_torrent})
bot.run()
