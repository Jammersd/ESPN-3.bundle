import datetime

NAME = 'ESPN 3'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

ESPN3_REPLAY = "http://espn.go.com/espn3/feeds/replay"
ESPN3_LIVE = "http://espn.go.com/espn3/feeds/live"
ESPN_PLAYER = "http://espn.go.com/watchespn/player/_/source/espn3/id/"

####################################################################################################
def Start():

	Plugin.AddPrefixHandler("/video/espn3", VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	MediaContainer.art = R(ART)
	MediaContainer.title1 = NAME
	DirectoryItem.thumb = R(ICON)

####################################################################################################
def VideoMainMenu():

	dir = MediaContainer(viewGroup="List")
	dir.Append(Function(DirectoryItem(VideoPage, "Live Games"), url = ESPN3_LIVE, predict="/event/event"))
	dir.Append(Function(DirectoryItem(VideoPage, "All Replay Games"), url = ESPN3_REPLAY, predict="/event/event"))
	dir.Append(Function(DirectoryItem(VideoPage, "Soccer"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='SO']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Football"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='FB']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Baseball"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='BB']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Basketball"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='BK']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Tennis"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='TN']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Hockey"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='HO']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Softball"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='SB']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Cricket"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='CR']/.."))
	dir.Append(Function(DirectoryItem(VideoPage, "Rugby"), url = ESPN3_REPLAY, predict="/event/event/sport[@code='RG']/.."))

	return dir

####################################################################################################
def VideoPage(sender, url, predict):

	if "live" in url:
		dir = MediaContainer(title2=sender.itemTitle, viewGroup="List", noCache=True)
	else:
		dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", noCache=True)

	content = XML.ElementFromURL(url, cacheTime=300).xpath(predict)
	eventMap = dict()

	for item in content:
		eventId = item.get('id')
		link = ESPN_PLAYER + eventId
		image = item.xpath('./thumbnail/large')[0].text
		title = item.xpath('./league')[0].text + ' - ' + item.xpath('./name')[0].text
		startTime = int(item.xpath('./startTimeGmtMs')[0].text)/1000
		subtitle = 'Originally Aired: ' + datetime.datetime.fromtimestamp(startTime).strftime('%a %b %d, %Y')
		eventList = eventMap.get(startTime)

		if eventList is None:
			eventList = []
			eventMap[startTime] = eventList

		# Tuple order here matters
		eventList.append((link, image, title, subtitle))

	events = eventMap.keys()[:]
	events.sort()
	events.reverse()

	for eventTime in events:
		for event in eventMap[eventTime]:
			# Same order they went into the tuple
			dir.Append(WebVideoItem(url=event[0], subtitle=event[3], title=event[2], thumb=Function(GetThumb, url=event[1])))

	return dir

####################################################################################################
def GetThumb(url):

	try:
		data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
		return DataObject(data, 'image/jpeg')
	except:
		pass

	return Redirect(R(ICON))
