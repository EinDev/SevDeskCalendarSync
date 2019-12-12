import configparser
import requests
import caldav
from caldav.elements import dav, cdav
import urllib.parse

config = configparser.ConfigParser()
config.read(['config.dist.ini', 'config.ini'])
print("SevDesk API-Token: " + config.get("sevdesk", "apikey"))

print("Zeige alle Rechnungen an:")
params = {
    'token': config.get("sevdesk", "apikey"),
    'limit': 1000,
    'offset': 0
}
response = requests.get('https://my.sevdesk.de/api/v1/Invoice', params=params)
if response.ok:
    jsonResponse = response.json()
    for invoice in jsonResponse['objects']:
        print(invoice)
calDavUrl = config.get('calendar', 'url')
print("Benuzte URL: %s" % calDavUrl)
client = caldav.DAVClient(calDavUrl, None, config.get('calendar', 'user'), config.get('calendar', 'pass'))
principal = client.principal()
calendars = principal.calendars()
print(calendars)
for cal in calendars:
    calendar_name = cal.get_properties([dav.DisplayName()])['{DAV:}displayname']
    section_name = 'calendar_' + calendar_name.replace(' ', '_')
    if section_name in config.sections():
        print("Price for %s: %.2f €" % (calendar_name, float(config.get(section_name, 'price'))))
        for event in cal.events():
            print("Ereignis: %s" % event)
    else:
        print("Calendar %s is not matched" % calendar_name)
