VIDEO_PREFIX = "/video/telebasel"

NAME = L('Title')

BASE_URL = "http://www.telebasel.ch/"
SHOW_LIST_URL = BASE_URL + "de/sendungen/"
LIVE_URL = BASE_URL + "ajaxHandler.php?action=live"

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = CACHE_1HOUR


def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")
    
    liveInfo = HTTP.Request(LIVE_URL).content
    Log(liveInfo)
    for line in liveInfo.splitlines():
        if line.find("***") >= 0:
            continue
        if line.find("SWFObject") >= 0:
            width = line.split('", "')[2]
            height = line.split('", "')[3]
        if line.find("addVariable") >= 0:
            url = line.split(',')[1][1:-7]
            break
            
    playerUrl = "/".join(url.split('/')[0:4])
    Log(playerUrl)
    clip = "/".join(url.split('/')[4:])
    Log(clip)
    dir.Append(RTMPVideoItem(playerUrl, clip=clip, width=width, height=height, live=True, title="TeleBasel Live-TV", thumb=R(ICON)))
    
    shows = HTML.ElementFromURL(SHOW_LIST_URL)
    for show in shows.xpath("//div[@class='ext-groups-showList']/div/div/div/a"):
        Log(HTML.StringFromElement(show))
        title = show.find("span").text
        Log(title)
        thumb = BASE_URL + show.find("img").get("src")
        Log(thumb)
        show_url = BASE_URL + show.get('href')
        Log(show_url)
        show_details = HTML.ElementFromURL(show_url).xpath("//div[@id='middle']/div[@id='content']//table//td")[0].findall("p")[1]
        Log(HTML.StringFromElement(show_details))
        summary = NoneStringHelper(show_details.text) + "\n\n" + NoneStringHelper(show_details.tail).strip()
        Log(summary)
        dir.Append(Function(DirectoryItem(ListEpisodes, title, summary=summary, thumb=thumb), url=show_url))

    return dir


def ListEpisodes(sender, url):
    dir = MediaContainer(viewGroup="InfoList", title2=sender.itemTitle)
    episodes = HTML.ElementFromURL(url)
    for episode in episodes.xpath("//div[@id='right']//div[contains(@class, 'padding')]"):
        Log(HTML.StringFromElement(episode))
        title = episode.findtext("div/a")
        Log(title)
        thumb = BASE_URL + episode.find("div[@class='img']").get("style").split("(")[1].strip(")")
        Log(thumb)
        video_url = BASE_URL + episode.find("div/div/a").get("href")
        Log(video_url)
        dir.Append(Function(VideoItem(GetEpisodeVideo, title, thumb=thumb), url=video_url))
    
    if len(dir) == 0:
        return MessageContainer("No episodes available", "There are no episodes for this show available.")
    return dir


def GetEpisodeVideo(sender, url):
    for show in HTML.ElementFromURL(url).xpath("//div[@class='ext-program']//script"):
        jsVars = show.text
        Log(jsVars)
        if jsVars.find('jwplayer("movieplayer").setup') >= 0:
            video_url = jsVars.split("file: ")[1].split('"')[1]
            Log(video_url)
            return Redirect(video_url)


def NoneStringHelper(string):
    return string if string else ""
