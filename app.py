from flask import Flask, send_file, jsonify, request
import requests as req, os

app = Flask(__name__)

SITES = [
    {"name":"Eksi Sozluk","url":"https://eksisozluk.com/biri/{u}","cat":["sosyal","topluluk"],"tr":True},
    {"name":"Teknopat","url":"https://www.technopat.net/members/{u}/","cat":["teknoloji"],"tr":True},
    {"name":"TurkHackTeam","url":"https://www.turkhackteam.org/members/{u}.html","cat":["hacking"],"tr":True},
    {"name":"Donanim Haber","url":"https://forum.donanimhaber.com/profil/{u}","cat":["teknoloji"],"tr":True},
    {"name":"Twitter X","url":"https://x.com/{u}","cat":["sosyal"],"tr":False},
    {"name":"Instagram","url":"https://www.instagram.com/{u}/","cat":["sosyal","fotograf"],"tr":False},
    {"name":"TikTok","url":"https://www.tiktok.com/@{u}","cat":["sosyal","video"],"tr":False},
    {"name":"YouTube","url":"https://www.youtube.com/@{u}","cat":["video"],"tr":False},
    {"name":"Facebook","url":"https://www.facebook.com/{u}","cat":["sosyal"],"tr":False},
    {"name":"LinkedIn","url":"https://www.linkedin.com/in/{u}","cat":["is","kariyer"],"tr":False},
    {"name":"Reddit","url":"https://www.reddit.com/user/{u}","cat":["sosyal","topluluk"],"tr":False},
    {"name":"Twitch","url":"https://www.twitch.tv/{u}","cat":["oyun","video"],"tr":False},
    {"name":"Kick","url":"https://kick.com/{u}","cat":["oyun","video"],"tr":False},
    {"name":"GitHub","url":"https://github.com/{u}","cat":["kodlama"],"tr":False},
    {"name":"GitLab","url":"https://gitlab.com/{u}","cat":["kodlama"],"tr":False},
    {"name":"HackerRank","url":"https://www.hackerrank.com/profile/{u}","cat":["kodlama"],"tr":False},
    {"name":"Codeforces","url":"https://codeforces.com/profile/{u}","cat":["kodlama"],"tr":False},
    {"name":"LeetCode","url":"https://leetcode.com/{u}/","cat":["kodlama"],"tr":False},
    {"name":"Replit","url":"https://replit.com/@{u}","cat":["kodlama"],"tr":False},
    {"name":"Codepen","url":"https://codepen.io/{u}","cat":["kodlama","web"],"tr":False},
    {"name":"Stack Overflow","url":"https://stackoverflow.com/users/{u}","cat":["kodlama"],"tr":False},
    {"name":"HackTheBox","url":"https://app.hackthebox.com/profile/{u}","cat":["hacking","CTF"],"tr":False},
    {"name":"TryHackMe","url":"https://tryhackme.com/p/{u}","cat":["hacking","CTF"],"tr":False},
    {"name":"BugCrowd","url":"https://bugcrowd.com/{u}","cat":["hacking"],"tr":False},
    {"name":"HackerOne","url":"https://hackerone.com/{u}","cat":["hacking"],"tr":False},
    {"name":"Steam","url":"https://steamcommunity.com/id/{u}","cat":["oyun"],"tr":False},
    {"name":"FACEIT","url":"https://www.faceit.com/tr/players/{u}","cat":["oyun","esports"],"tr":False},
    {"name":"OP.GG","url":"https://www.op.gg/summoners/tr/{u}","cat":["oyun"],"tr":False},
    {"name":"Chess.com","url":"https://www.chess.com/member/{u}","cat":["oyun","satranc"],"tr":False},
    {"name":"Lichess","url":"https://lichess.org/@/{u}","cat":["oyun","satranc"],"tr":False},
    {"name":"Roblox","url":"https://www.roblox.com/user.aspx?username={u}","cat":["oyun"],"tr":False},
    {"name":"NameMC","url":"https://namemc.com/profile/{u}","cat":["oyun","minecraft"],"tr":False},
    {"name":"PSN Profiles","url":"https://psnprofiles.com/{u}","cat":["oyun","playstation"],"tr":False},
    {"name":"Spotify","url":"https://open.spotify.com/user/{u}","cat":["muzik"],"tr":False},
    {"name":"SoundCloud","url":"https://soundcloud.com/{u}","cat":["muzik"],"tr":False},
    {"name":"Last.fm","url":"https://www.last.fm/user/{u}","cat":["muzik"],"tr":False},
    {"name":"Bandcamp","url":"https://{u}.bandcamp.com","cat":["muzik"],"tr":False},
    {"name":"Medium","url":"https://medium.com/@{u}","cat":["blog"],"tr":False},
    {"name":"Substack","url":"https://{u}.substack.com","cat":["blog"],"tr":False},
    {"name":"Tumblr","url":"https://{u}.tumblr.com","cat":["sosyal","blog"],"tr":False},
    {"name":"DeviantArt","url":"https://www.deviantart.com/{u}","cat":["sanat"],"tr":False},
    {"name":"Behance","url":"https://www.behance.net/{u}","cat":["sanat","tasarim"],"tr":False},
    {"name":"Dribbble","url":"https://dribbble.com/{u}","cat":["sanat","tasarim"],"tr":False},
    {"name":"ArtStation","url":"https://www.artstation.com/{u}","cat":["sanat","oyun"],"tr":False},
    {"name":"Pixiv","url":"https://www.pixiv.net/en/users/{u}","cat":["sanat","anime"],"tr":False},
    {"name":"Flickr","url":"https://www.flickr.com/people/{u}/","cat":["fotograf"],"tr":False},
    {"name":"500px","url":"https://500px.com/p/{u}","cat":["fotograf"],"tr":False},
    {"name":"Pinterest","url":"https://www.pinterest.com/{u}/","cat":["sosyal","alisveris"],"tr":False},
    {"name":"Wattpad","url":"https://www.wattpad.com/user/{u}","cat":["blog","kitap"],"tr":False},
    {"name":"Goodreads","url":"https://www.goodreads.com/{u}","cat":["kitap"],"tr":False},
    {"name":"MyAnimeList","url":"https://myanimelist.net/profile/{u}","cat":["anime","manga"],"tr":False},
    {"name":"AniList","url":"https://anilist.co/user/{u}","cat":["anime","manga"],"tr":False},
    {"name":"Patreon","url":"https://www.patreon.com/{u}","cat":["icerik uretici"],"tr":False},
    {"name":"Ko-fi","url":"https://ko-fi.com/{u}","cat":["icerik uretici"],"tr":False},
    {"name":"Linktree","url":"https://linktr.ee/{u}","cat":["sosyal"],"tr":False},
    {"name":"Kaggle","url":"https://www.kaggle.com/{u}","cat":["kodlama","veri bilimi"],"tr":False},
    {"name":"Hugging Face","url":"https://huggingface.co/{u}","cat":["yapay zeka","kodlama"],"tr":False},
    {"name":"Docker Hub","url":"https://hub.docker.com/u/{u}","cat":["kodlama","devops"],"tr":False},
    {"name":"DEV.to","url":"https://dev.to/{u}","cat":["kodlama","blog"],"tr":False},
    {"name":"Freelancer","url":"https://www.freelancer.com/u/{u}","cat":["is","freelance"],"tr":False},
    {"name":"Upwork","url":"https://www.upwork.com/fl/{u}","cat":["is","freelance"],"tr":False},
    {"name":"Fiverr","url":"https://www.fiverr.com/{u}","cat":["is","freelance"],"tr":False},
    {"name":"Etsy","url":"https://www.etsy.com/shop/{u}","cat":["alisveris"],"tr":False},
    {"name":"eBay","url":"https://www.ebay.com/usr/{u}","cat":["alisveris"],"tr":False},
    {"name":"Tinder","url":"https://tinder.com/@{u}","cat":["dating","sosyal"],"tr":False},
    {"name":"Badoo","url":"https://badoo.com/profile/{u}","cat":["dating"],"tr":False},
    {"name":"OkCupid","url":"https://www.okcupid.com/profile/{u}","cat":["dating"],"tr":False},
    {"name":"Strava","url":"https://www.strava.com/athletes/{u}","cat":["spor","kosu"],"tr":False},
    {"name":"TripAdvisor","url":"https://www.tripadvisor.com.tr/Profile/{u}","cat":["seyahat"],"tr":False},
    {"name":"Duolingo","url":"https://www.duolingo.com/profile/{u}","cat":["egitim","dil"],"tr":False},
    {"name":"Codecademy","url":"https://www.codecademy.com/profiles/{u}","cat":["kodlama","egitim"],"tr":False},
    {"name":"TradingView","url":"https://tr.tradingview.com/u/{u}/","cat":["finans","kripto"],"tr":False},
    {"name":"OpenSea","url":"https://opensea.io/{u}","cat":["kripto","nft"],"tr":False},
    {"name":"Paribu","url":"https://www.paribu.com/user/{u}","cat":["kripto","finans"],"tr":True},
    {"name":"BtcTurk","url":"https://www.btcturk.com/profil/{u}","cat":["kripto","finans"],"tr":True},
    {"name":"Trendyol","url":"https://www.trendyol.com/profil/{u}","cat":["alisveris"],"tr":True},
    {"name":"Hepsiburada","url":"https://www.hepsiburada.com/profil/{u}","cat":["alisveris"],"tr":True},
    {"name":"Sahibinden","url":"https://www.sahibinden.com/profil/{u}","cat":["alisveris","ilan"],"tr":True},
    {"name":"Dolap","url":"https://dolap.com/{u}","cat":["alisveris","moda"],"tr":True},
    {"name":"Kariyer.net","url":"https://www.kariyer.net/cv/{u}","cat":["is","kariyer"],"tr":True},
    {"name":"Sikayetvar","url":"https://www.sikayetvar.com/kullanici/{u}","cat":["tuketici"],"tr":True},
    {"name":"Beyaz Perde","url":"https://www.beyazperde.com/kullaniciler/{u}/","cat":["sinema","video"],"tr":True},
    {"name":"Nefis Yemek","url":"https://www.nefisyemektarifleri.com/profil/{u}/","cat":["yemek"],"tr":True},
    {"name":"Yemeksepeti","url":"https://www.yemeksepeti.com/profil/{u}","cat":["yemek"],"tr":True},
    {"name":"Sporx","url":"https://www.sporx.com/profil/{u}","cat":["spor"],"tr":True},
    {"name":"Itch.io","url":"https://{u}.itch.io","cat":["oyun","indie"],"tr":False},
    {"name":"GameJolt","url":"https://gamejolt.com/@{u}","cat":["oyun","indie"],"tr":False},
    {"name":"NexusMods","url":"https://www.nexusmods.com/users/{u}","cat":["oyun","mod"],"tr":False},
    {"name":"Speedrun.com","url":"https://www.speedrun.com/user/{u}","cat":["oyun"],"tr":False},
    {"name":"SketchFab","url":"https://sketchfab.com/{u}","cat":["3D","sanat"],"tr":False},
    {"name":"Mastodon","url":"https://mastodon.social/@{u}","cat":["sosyal"],"tr":False},
    {"name":"Bluesky","url":"https://bsky.app/profile/{u}","cat":["sosyal"],"tr":False},
    {"name":"Threads","url":"https://www.threads.net/@{u}","cat":["sosyal"],"tr":False},
    {"name":"VK","url":"https://vk.com/{u}","cat":["sosyal"],"tr":False},
    {"name":"Product Hunt","url":"https://www.producthunt.com/@{u}","cat":["teknoloji","startup"],"tr":False},
    {"name":"IndieHackers","url":"https://www.indiehackers.com/{u}","cat":["startup","is"],"tr":False},
    {"name":"AngelList","url":"https://angel.co/u/{u}","cat":["is","startup"],"tr":False},
    {"name":"Keybase","url":"https://keybase.io/{u}","cat":["guvenlik"],"tr":False},
    {"name":"Quora","url":"https://www.quora.com/profile/{u}","cat":["sosyal","egitim"],"tr":False},
    {"name":"Vimeo","url":"https://vimeo.com/{u}","cat":["video","sinema"],"tr":False},
    {"name":"Dailymotion","url":"https://www.dailymotion.com/{u}","cat":["video"],"tr":False},
    {"name":"Puhutv","url":"https://puhutv.com/profil/{u}","cat":["video","dizi"],"tr":True},
    {"name":"BluTV","url":"https://www.blutv.com/profil/{u}","cat":["video","dizi"],"tr":True},
    {"name":"Milliyet Blog","url":"https://blog.milliyet.com.tr/{u}","cat":["blog","haber"],"tr":True},
    {"name":"Crunchyroll","url":"https://www.crunchyroll.com/user/{u}","cat":["anime","video"],"tr":False},
    {"name":"ResearchGate","url":"https://www.researchgate.net/profile/{u}","cat":["akademik"],"tr":False},
    {"name":"Academia.edu","url":"https://independent.academia.edu/{u}","cat":["akademik","egitim"],"tr":False},
    {"name":"Instructables","url":"https://www.instructables.com/member/{u}/","cat":["maker","DIY"],"tr":False},
    {"name":"Hackster.io","url":"https://www.hackster.io/{u}","cat":["donanim","IoT"],"tr":False},
    {"name":"XDA Developers","url":"https://forum.xda-developers.com/member.php?username={u}","cat":["android","teknoloji"],"tr":False},
]

H = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.7",
    "DNT": "1",
}

def chk(site, u):
    url = site["url"].replace("{u}", u)
    try:
        r = req.get(url, headers=H, timeout=8, allow_redirects=True)
        s, body = r.status_code, r.text.lower()[:3000] if r.text else ""
        if s == 404: return False
        bad = ["not found","bulunamadi","doesn't exist","does not exist","no user","account not found"]
        if s == 200:
            for x in bad:
                if x in body: return False
            if u.lower() in body: return True
            return None
        if s in [403, 429, 503]: return None
        return False
    except:
        return None

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/count")
def count():
    return jsonify({"count": len(SITES)})

@app.route("/api/check", methods=["POST"])
def api_check():
    d = request.json
    u, i = d.get("username","").strip(), d.get("idx",0)
    if not u or i >= len(SITES):
        return jsonify({"error":"invalid"}), 400
    site = SITES[i]
    result = chk(site, u)
    return jsonify({
        "name": site["name"],
        "url": site["url"].replace("{u}", u),
        "cat": site["cat"],
        "tr": site["tr"],
        "found": result
    })

if __name__ == "__main__":
    import socket
    try: ip = socket.gethostbyname(socket.gethostname())
    except: ip = "127.0.0.1"
    print(f"\n  VERVAIN calisiyor!")
    print(f"  Tarayici: http://localhost:5000")
    print(f"  Toplam site: {len(SITES)}\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
