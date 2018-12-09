import praw
import getpass
from keys import *

password = getpass.getpass()

mod = praw.Reddit(
    client_id=MOD_CLIENT_ID,
    client_secret=MOD_CLIENT_SECRET,
    user_agent="report-mod-bot",
    username="VRCbot",
    password=password)

user = praw.Reddit(
    client_id=USER_CLIENT_ID,
    client_secret=USER_CLIENT_SECRET,
    user_agent="report-user-bot",
    username=USER,
    password=PWD)

report_stream = \
    praw.models.util.stream_generator(
        mod.subreddit("dota2").mod.reports,
        pause_after=None,
        skip_existing=False)

user_subreddit = user.subreddit("dota2")

for report in report_stream:
    print(report)
    if len(report.mod_reports) == 0:
        continue

    print("Mod Reports: {}".format(report.mod_reports))
    message = ""
    mods = []
    for [reason, mod] in report.mod_reports:
        if mod == "AutoModerator":
            continue

        message += "* {} for {}\n".format(mod, reason)
        mods.append(mod)

    if len(mods) > 0:
        message = "[This submission]({}) received a report from: \n\n".format(report.link_permalink) + message
        title = "Report from {}".format(", ".join(mods))
        print(mods, message)
        #user_subreddit.message(title, message)
