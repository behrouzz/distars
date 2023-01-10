
def create_hovertext(df):
    h = '<b>'+df['main_id'].str.replace('"','')+'</b><br>' + \
        'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str) + '<br>' \
        'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str) + '<br>'\
        'Distance: '+df['r'].apply(lambda x: round(x,3)).astype(str)+' <i>(pc)</i><br>' + \
        'Parallax: '+df['plx_value'].astype(str)+' <i>(mas)</i><br>'
    return h

