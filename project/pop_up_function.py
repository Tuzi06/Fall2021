##
import folium

def location_map_path(df):
    fg = folium.FeatureGroup("location")
    loc= "location"
    LAT=list(df['lat'])
    LON=list(df['lon'])
    for lt,ln in zip(LAT,LON):
        fg.add_child(folium.Marker(location=[lt,ln],popup=loc))
    fg.add_child(folium.PolyLine(df[['lat','lon']], color='blue'))
    return fg


def map_pop_up(df,fg1):
    LAT=list(df['lat'])
    LON=list(df['lon'])
    name=list(df['name'])
    opening_hour=list(df['opening_hours'])
    opening_hour=['None' if v is None else v for v in opening_hour]
    website=list(df['website'])
    website=['None' if v is None else v for v in website]
    
    for lt,ln,nm,op,ws in zip(LAT,LON,name,opening_hour,website):
        if (op!='None')&(ws!='None'):
            ws = list(ws)
            if (ws[-1] == "/"):
                ws[-1] = ""
                ws = ''.join(ws)
            else:
                ws = ''.join(ws)
            #print(ws)

            fg1.add_child(folium.Marker([lt,ln ],popup="<b>name:</b>"+nm+"\n"+"<br> <b>opening hours is : </b>"+op+"\n"+"<br><b>website link: </b><a href="+ws+">click here</a>",tooltip="Click me!",icon=folium.Icon(color="green")))

        elif (op!='None')&(ws=='None'):
            fg1.add_child(folium.Marker([lt,ln ],popup="<b>name:</b>"+nm+"\n"+"<br> <b>opening hours is : </b>"+op+"\n",icon=folium.Icon(color="green")))

        elif (op=='None')&(ws=='None'):
            fg1.add_child(folium.Marker([lt,ln ],popup="<b>name:</b>"+nm+"\n",icon=folium.Icon(color="green")))

        elif (op=='None')&(ws!='None'):
            ws = list(ws)
            if (ws[-1] == "/"):
                ws[-1] = ""
                ws = ''.join(ws)
            else:
                ws = ''.join(ws)
            #print(ws)
            fg1.add_child(folium.Marker([lt,ln ],popup="<b>name:</b>"+nm+"\n"+"<br><b>website link: </b><a href="+ws+">click here</a>",tooltip="Click me!",icon=folium.Icon(color="green")))
    return fg1 