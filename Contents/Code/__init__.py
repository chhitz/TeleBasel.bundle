VIDEO_PREFIX = "/video/telebasel"

NAME = L('Title')

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
    dir.Append(Function(DirectoryItem(CallbackExample,"directory item title", subtitle="subtitle", summary="clicking on me will call CallbackExample", thumb=R(ICON), art=R(ART))))


    return dir

def CallbackExample(sender):

    return MessageContainer("Not implemented","In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle)

  
