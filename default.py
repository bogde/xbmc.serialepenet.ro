import urllib, re, xbmcplugin, xbmcgui, xbmcaddon, time
from bs4 import BeautifulSoup
import requests
import subtitles

# serialepenet.ro

# plugin constants
__version__     = "1.0"
__plugin__      = "serialepenet.ro" + __version__
__base_url__    = "http://serialepenet.ro"
__settings__    = xbmcaddon.Addon(id = "plugin.video.serialepenet.ro")
__addonname__   = "serialepenet.ro"
__agent__       = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
__code__        = __settings__.getSetting("code")

#def log(txt):
#    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
#    xbmc.log(msg = message, level = xbmc.LOGDEBUG)

def MAINMENU():
    addDir("Seriale", "/seriale", 0, "")
    if __settings__.getSetting("last_link"):
        addDir(__settings__.getSetting("last_title"), __settings__.getSetting("last_link"), 2, "")
    addDir("Cautare", "/cautare", 0, "")
    #addDir("Top", "/top", 0, "")
    addLink('Activare', "/activare", "", "", "activare", "", False)
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def ACTIVATE():
    code = __settings__.getSetting("code")
    print "code: ", code
    __settings__.openSettings()
    code = __settings__.getSetting("code")
    print "code: ", code
    __code__ = code
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def SEARCH():
    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault("")
    kb.setHeading("Cautare")
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        term = kb.getText()
        r = s.get(__base_url__ + "/search/node/" + urllib.quote(term))

        print r.status_code
        
        if r.status_code == 200:
            page = r.content

            # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
            page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)

            soup = BeautifulSoup(page)
            movies = soup.find(attrs={"class": "search-results node-results"})

            for movie in movies.findAll('div', attrs={"class": "bloc_seriale"}):
                try:
                    print movie.text, movie.a['href'], movie.img['src']
                    addDir(movie.text, "/" + movie.a['href'], 2, __base_url__ + "/" + movie.img['src'])
                except:
                    # we will probably miss some series; to fix later
                    pass
                
            xbmc.executebuiltin("Container.SetViewMode(500)")
        else:
            showError(__base_url__ + url, r)
    else:
        print "closed"
              
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def CATEGORIES():
    r = s.get(__base_url__)

    if r.status_code == 200:
        page = r.content

        # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
        page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)
                
        soup = BeautifulSoup(page)
        insidebar = soup.find(id="inside_sidebar")

        for div in insidebar.findAll('span', 'field-content'):
            for a in div.findAll('a'):
                addDir(a.text, a['href'], 1, '')
    else:
        showError(__base_url__, r)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)
                
def CATEGORY(url):
    r = s.get(__base_url__ + url)
        
    if r.status_code == 200:
        page = r.content

        # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
        page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)

        soup = BeautifulSoup(page)
        movies = soup.find(attrs={"class": "menu"})

        for movie in movies.findAll('div', attrs={"class": "bloc_seriale"}):
            try:
                print movie.text, movie.a['href'], movie.img['src']
                addDir(movie.text, "/" + movie.a['href'], 2, __base_url__ + "/" + movie.img['src'])
            except:
                # we will probably miss some series; to fix later
                pass
    else:
        showError(__base_url__ + url, r)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def SEASONS(url):
    r = s.get(__base_url__ + url)
        
    if r.status_code == 200:
        page = r.content

        # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
        page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)
                
        soup = BeautifulSoup(page)

        # get the title and save "last watched" setting
        title = soup.title.text.split("serial online cu subtitrare")[0].strip()
        __settings__.setSetting('last_link', url)
        __settings__.setSetting('last_title', title)
        
        movies = soup.find(attrs={"class": "menu"})

        for movie in movies.findAll('div', attrs={"class": "bloc_sezoane"}):
            try:
                print movie.text, movie.a['href']
                addDir(movie.text, "/" + movie.a['href'], 3, '')
            except:
                pass
    else:
        showError(__base_url__ + url, r)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def CLIPS(url):
    print "++++ clips, getting page"
    r = s.get(__base_url__ + url)
        
    if r.status_code == 200:
        page = r.content
        
        print "++++ removing trafic.ro script"
        # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
        page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)

        print "++++ making soup"
        soup = BeautifulSoup(page)
        print "++++ finding section"
        movies = soup.find(attrs={"class": "menu"})

        print "++++ extracting data"
        for movie in movies.findAll('div', attrs={"class": "bloc_episoade"}):
            try:
                print movie.text, movie.a['href'], movie.img['src']
                addDir(movie.text, movie.a['href'], 4, __base_url__ + "/" + movie.img['src'])
            except:
                pass
        print "++++ done"
    else:
        showError(__base_url__ + url, r)

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def VIDEOLINKS(url):
    print "++++ videolinks"

    if not __code__:
        print "----- no code entered"
        print "----- getting page with no code"
        r = s.get(__base_url__ + url)
        print "----- done getting page"
    else:
        payload = {'cod': __code__, 'activare': 'Activeaza'}
        print payload
        headers = {'User-Agent': __agent__, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Referer': __base_url__ + url, 'Content-Type': 'application/x-www-form-urlencoded'}
        print "+++++ getting page"
        r = requests.post(__base_url__ + url, data = payload, headers = headers)
        print "+++++ done"

    if r.status_code == 200:
        cookiestr = ""
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        for x in cookies:
            cookiestr = cookiestr + x + ":" + cookies.get(x) + "; "
                    
        page = r.content

        print "++++ removing trafic.ro script"       
        # remove the trafic.ro script; otherwise, for some reason parsing fails in XBMC, although it works in IDLE
        page = re.sub("<div id=\"trafic_ro\">((.|\n)*)</div>", "", page)

        print "++++ making soup"
        soup = BeautifulSoup(page)

        print "++++ check for activation message"
        error = soup.find("div", {"id": "header_sms"})
        if not error:
            print "++++ finding links"
            movie = soup.find(attrs={"class": "leanback-player-video"})

            print movie.source['src']
            print movie.track['src']
            print "++++ done"

            addLink('Da click pentru vizionare', movie.source['src'], __base_url__ + movie.track['src'], '', 'play_video', cookiestr, False)
        else:
            print "activation nedeed !!!"
            line1 = "Pentru a vedea episodul trebuie sa obtii un cod de acces"
            line2 = "de pe serialepenet.ro si sa-l introduci in sectiunea Activare!"
            xbmcgui.Dialog().ok(__addonname__, line1, line2, "")
    else:
        showError(__base_url__ + url, r)  

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc = False)

def get_params():
    param = []
    paramstring = sys.argv[2]
    
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace("?", "")
        if (params[len(params) - 1] == "/"):
            params = params[0 : len(params) - 2]
        pairsofparams = cleanedparams.split("&")
        param={}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split("=")
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
                                
    return param

def addLink(name, url, subtitle, iconimage, action, cookies, watched):
    ok = True
    url = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&subtitle=" + subtitle + "&action=" + str(action) + "&cookies=" + cookies + "&name=" + urllib.quote_plus(name)
    print "~~~~~~~~~~~~", url
    liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage=iconimage)
    infolabels = {}
    infolabels["Title"] = name
    liz.setInfo(type="Video", infoLabels = infolabels)
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = liz)
    return ok

def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
    liz.setInfo(type="Video", infoLabels = { "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
    return ok
        
def showError(url, r):
    line1 = "An error occured while accessing:"
    line2 = "Status: " + str(r.status_code) + " " + r.reason
    xbmcgui.Dialog().ok(__addonname__, line1, url, line2)
    url = ""


s = requests.Session()
s.headers.update({'User-Agent': __agent__})

params = get_params()
print ">>>>>>>>>>> params = ", params
url         = None
name        = None
mode        = None
action      = None
cookies     = None
subtitle    = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    action = str(params["action"])
except:
    pass
try:
    cookies = str(params["cookies"])
    cookies = cookies.replace(":", "=")
    cookies = cookies.strip()
    cookies = cookies.rstrip(";")
except:
    pass
try:
    subtitle = str(params["subtitle"])
except:
    pass

print "**** Mode:\t" + str(mode)
print "**** URL:\t" + str(url)
print "**** Name:\t" + str(name)
print "**** Action:\t" + str(action)
print "**** Cookie:\t" + str(cookies)
print "**** Subtitle:\t" + str(subtitle)

if mode == None or url == None or len(url) < 1:
    MAINMENU()
        
elif mode == 0 and url == "/seriale":
    CATEGORIES()
    
elif mode == 0 and url == "/cautare":
    SEARCH()
    
elif mode == 1:
    print "" + url
    CATEGORY(url)
        
elif mode == 2:
    print "" + url
    SEASONS(url)

elif mode == 3:
    print "" + url
    CLIPS(url)

elif mode == 4:
    print "" + url
    VIDEOLINKS(url + "?html5")

if action == 'play_video':
    url = url + '?start=0'
    print url

    headers = "User-Agent=" + __agent__ + "&Cookie=" + cookies + "&Referer=http://serialepenet.ro/476-embed-236/player/player.swf"

    url = url + "|" + headers;
    print url

    player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER) 
    player.play(url)

    headers = {'User-Agent': __agent__}
    print "--- getting subtitle file"
    r = requests.get(subtitle, headers=headers)
    print "--- done"
    text = r.content
    print "--- converting subtitles"
    subt = subtitles.ttml2srt(text, "test.srt")
    print "--- done: ", subt

    player.setSubtitles(subt)

    while not player.isPlaying():
        time.sleep(1)
        
elif action == 'activare':
    ACTIVATE()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
