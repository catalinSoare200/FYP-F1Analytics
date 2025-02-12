import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from bs4 import BeautifulSoup
import re
import plotly.graph_objects as go


st.set_page_config(page_title='F1 Analytics Dashboard', layout='wide')

# Define paths
DATA_PATH = "C:/Users/Catalin/Desktop/FYp/CleanData"

# Load data
@st.cache_data
def load_data(filename, index_col=None):
    df =pd.read_csv(os.path.join(DATA_PATH,filename), index_col=index_col)
    
    df.columns =df.columns.str.strip().str.lower()  
    return df

#loading datasets
drivers_df =load_data("drivers.csv")

teams_df= load_data("constructors.csv" )
races_df = load_data("races.csv")
results_df =load_data("results.csv")
qualifying_df= load_data("qualifying.csv")
standings_df =load_data("driver_standings.csv")
pitstops_df =load_data("pit_stops.csv")
lap_times_df= load_data("lap_times.csv")
tracks_df =load_data("circuits.csv")
constructor_results_df= load_data("constructor_results.csv")
constructor_standings_df= load_data("constructor_standings.csv")
sprint_results_df =load_data("sprint_results.csv")
seasons_df =load_data("seasons.csv")
status_df = load_data("status.csv")


st.markdown("""
    <style>
        .main-menu {text-align:center; font-size: 60px; font-weight: bold; padding: 10px; color: black; font-family: 'Arial Black', sans-serif;}
        .main-menu1{text-align: center; font-size:  60px; font-weight: bold; padding: 10px; color: red; font-family: 'Arial Black', sans-serif;}
        .css-18e3th9 {padding-top: 2rem;}
        .driver-info {font-size: 33px; font-weight:bold; margin-bottom: 10px; color: black;}
        .driver-info1 {font-size: 33px;text-align:left; font-weight: bold; margin-bottom: 10px; color: black;}
        .stApp {background-color: white; color: black;}
        .highlight {color: red; font-weight: bold;}
        .sidebar .sidebar-content {width: 300px; font-size: 60px; font-family: 'Arial' , sans-serif;}
        .stSidebar {background-color: white; color:black; font-size:50px;font-family: 'Arial', sans-serif;}
        .stTitle {color: black; text-align: left;font-size: 50px; font-weight: bold; }
            
    </style>
""",  unsafe_allow_html=True)



menu= ['Home','Driver Info','Team Info', 'Tracks','Simulated Races' ]
st.sidebar.title("Navigation")

choice =st.sidebar.radio("", menu,index=0)

#get driver image from wikipedia
def get_wikipedia_image(wiki_url):

    if not isinstance(wiki_url, str) or not wiki_url.startswith("http"):
        return None
    

    response =requests.get(wiki_url)
    if response.status_code != 200:
        return None
    

    soup= BeautifulSoup(response.text,'html.parser'  )
    infobox =soup.find('table',{'class': 'infobox'})
    
    if infobox:
        img_tag =infobox.find('img')

        if img_tag:

            return "https:" + img_tag['src']
    
    return None



#Home PG
def home():

    
    imagePath ="C:/Users/Catalin/Desktop/FYp/OtherImg/UoW.png"
    st.image(imagePath, caption="University of Westminster",   width=500 )

    st.markdown("<p class='main-menu'>🏁 Formula 1 Analytical Dashboard 🏁</p>", unsafe_allow_html=True   )

    st.markdown( "<p class='main-menu1'>Catalin Soare - (W1924815)</p>", unsafe_allow_html=True)

    st.markdown("<p class='main-menu1'> </p>", unsafe_allow_html=True)
    st.markdown("<p class='main-menu1'> </p>", unsafe_allow_html=True)
    

    st.markdown("""
        <p style="font-size:44px; font-weight:bold; text-align:center;">
        This dashboard provides insights into Formula 1 statistics:
        </p>
                
        <p>    </p>
        <p>    </p>
                
        
       
       <p style="font-size:44px; font-weight:bold;text-align:center;"> Using the <span style="color:red;">sidebar navigation</span> you can explore different sections!       </p>
                
    """, unsafe_allow_html=True)



# Driver Info PG
def driver_info():
    
    st.markdown("<p class='stTitle'>Driver Information</p>" , unsafe_allow_html=True)
    
    # Select driver
    drivers_df['full_name'] =drivers_df['forename'] + ' ' + drivers_df['surname' ]

    selected_driver =st.sidebar.selectbox('Select a Driver' , drivers_df['full_name'].unique(),index= 0 )
    driver_row =drivers_df[drivers_df['full_name']== selected_driver].iloc[0]

    
    #Get driver image from wikipedia
    wikiUrl =driver_row.get('url', None)
    image_url = get_wikipedia_image(wikiUrl) if wikiUrl else None
    st.markdown(f"<p class= 'driver-info1'><span class = 'highlight'>Full Name: </span> {driver_row['full_name']}</p>",unsafe_allow_html= True )
    col1,col2= st.columns([1, 2])

    with col1:

        if image_url:

            st.image(  image_url,caption=selected_driver,width=400)

        else:

            st.write("No image available for this specific driver.")
        
    with col2:

        total_races= results_df[results_df['driverid'] ==driver_row['driverid']].shape[0]

        total_wins =results_df[(results_df['driverid'] == driver_row['driverid'])& (results_df['positionorder']== 1)].shape[0]

        podiums=results_df[(results_df['driverid']== driver_row['driverid']) &(results_df['positionorder']<= 3)].shape[0]

        avg_finish =results_df[results_df['driverid'] == driver_row['driverid']]['positionorder'].mean()

        avg_qualifying = qualifying_df[qualifying_df['driverid'] == driver_row['driverid']]['position'].mean()

        team_names =teams_df[ teams_df['constructorid'].isin(results_df[results_df['driverid'] == driver_row['driverid']]['constructorid'].unique())][ 'name' ].unique()
        
        
        st.markdown(f"<p class='driver-info'><span class='highlight'>Nationality:</span>{driver_row['nationality']} </p>", unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Date of Birth:</span>{driver_row['dob']} </p>",unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Total Races:</span>{total_races}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Total Wins:</span>{total_wins}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Podiums:</span> {podiums}</p>",unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Avg Finish Position:</span> {avg_finish:.2f}  </p>", unsafe_allow_html=True)
        st.markdown(f"<p class='driver-info'><span class='highlight'>Avg Qualifying Position:</span> {avg_qualifying:.2f}</p>", unsafe_allow_html=True)

        st.markdown(f"<p class='driver-info'><span class='highlight'>Teams:</span> {', '.join(team_names)}</p>", unsafe_allow_html=True)
    
    #Graphs
    driver_results= results_df[ results_df['driverid'] ==driver_row['driverid']]


    driver_results =driver_results.merge(races_df[['raceid', 'date']], on='raceid', how='left')
    
    driver_results['date'] =pd.to_datetime(driver_results['date'])


    driver_results =driver_results.sort_values(by='date')

    fig1 = px.line(driver_results,x='date',   y='points',   title=f'Average Points per Race Over Time for  {selected_driver}',
                   line_shape='spline',  markers=True,   color_discrete_sequence=['#ff0000'])
    

    
    position_counts= driver_results['positionorder'].value_counts().sort_index()

    fig2 =px.bar(x=position_counts.index, y=position_counts.values, labels={'x': 'Finishing Position', 'y': 'Count'},
                 
                  title=f'Finishing Position Distribution for {selected_driver}', color_discrete_sequence=['#ff0000'])
    


    col3,col4 =st.columns(2)


    with col3:

        st.plotly_chart(fig1,  use_container_width=True)

    with col4:

        st.plotly_chart(fig2,use_container_width=True)

#Get team logo from Wikipedia
def get_team_logo(wiki_url):
    if not isinstance(wiki_url, str) or not wiki_url.startswith("http"):

        return None


    try:

        response=requests.get(wiki_url )

        if response.status_code !=200:

            return None

        soup= BeautifulSoup(response.text, 'html.parser')
        infobox  =soup.find('table',{'class': 'infobox'})


        if infobox:
            img_tags= infobox.find_all('img')

            #look for logo in file name
            for img in img_tags:

                img_url ="https:" +img['src']

                if "logo" in img_url.lower() or "badge" in img_url.lower():#common words

                    return img_url

            #return first image if no logo
            return "https:" +img_tags[0]['src'] if img_tags else None
        


    except Exception as e:

        return None

    return None




#Team Info PG
def team_info():
    
    st.markdown("<p class='stTitle'>Team Information</p>",unsafe_allow_html= True)
    st.write( "Details about constructors and their performance." )

    #check name exists
    drivers_df['full_name'] =drivers_df['forename'] + ' ' + drivers_df['surname' ]

    #dropdown
    selected_team= st.sidebar.selectbox('Select a Team',  teams_df['name'].unique(), index=  0)
    team_row= teams_df[teams_df['name'] ==selected_team].iloc[0 ]


    #get team logo from wiki
    wiki_url =team_row.get('url', None)
    logo_url= get_team_logo(wiki_url) if wiki_url else None



    #filtering res
    team_results =results_df[results_df['constructorid' ] ==team_row['constructorid' ]]

    team_standings= constructor_standings_df[constructor_standings_df['constructorid'] ==team_row['constructorid'] ]

    team_constructor_results =constructor_results_df[constructor_results_df['constructorid' ]== team_row['constructorid']]

    #key stats calculation
    total_races =team_results.shape[0]

    total_wins =team_results[team_results['positionorder'] == 1].shape[0]

    podiums= team_results[team_results['positionorder'] <= 3].shape[0]
    avg_finish= team_results['positionorder'].mean() if not team_results.empty else None


    total_points= team_constructor_results['points'].sum() if not team_constructor_results.empty else 0
    championships =team_standings[team_standings['position']== 1].shape[0] if not team_standings.empty else 0 

    #get drivers per team
    team_driver_ids =team_results['driverid' ].unique()

    team_drivers =drivers_df[drivers_df['driverid' ].isin(team_driver_ids)]['full_name' ].unique()
    col1,col2=st.columns([1,2])
    

    with col1:

        st.markdown(f"<p class='driver-info1'><span class = 'highlight'>Team Name:</span> {team_row['name']}</p>", unsafe_allow_html=True)

        if logo_url:

            st.image(logo_url,caption=  selected_team,width= 600)

        else:
            st.write("No image available for this team." )


    with col2:

        st.markdown(f"<p class='driver-info'><span class='highlight' >Nationality:</span> {team_row['nationality']}</p>",unsafe_allow_html=True  )

        st.markdown(f"<p class='driver-info'><span class='highlight'>Total Races:</span>{total_races}</p>",unsafe_allow_html=True )

        st.markdown(f"<p class='driver-info'><span class='highlight'>Total Wins:</span> {total_wins}</p>", unsafe_allow_html=True)

        st.markdown(f"<p class='driver-info'><span class='highlight'>Podiums:</span> {podiums}</p>",unsafe_allow_html=True )

        if avg_finish:

            st.markdown(f"<p class='driver-info'><span class='highlight'>Avg Finish Position:</span>{avg_finish:.2f}</p>",unsafe_allow_html = True )

        st.markdown(f"<p class='driver-info'><span class='highlight'>Total Points:</span> {total_points}</p>",unsafe_allow_html= True)

        st.markdown(f"<p class='driver-info'><span class='highlight'>Championships Won:</span> {championships}</p>" ,unsafe_allow_html= True )
        
    st.markdown(f"<p class='driver-info'><span class='highlight'>Drivers:</span>{', '.join(team_drivers)}</p>",unsafe_allow_html =True )


    #Graphs
    if not team_results.empty:

        team_results =team_results.merge(races_df[['raceid','date'] ],on='raceid',how='left')

        team_results['date' ] =pd.to_datetime(team_results['date' ] )


        team_results= team_results.sort_values(by='date')

        #points
        fig1= px.line(team_results, x='date',y='points', title=f'Points Over Time for {selected_team}', line_shape='spline', markers=True,color_discrete_sequence=['#0000FF'] )

        # Finishing Position Distribution
        position_counts =team_results['positionorder'].value_counts().sort_index()

        fig2 =px.bar(x=position_counts.index, y=position_counts.values,labels={'x': 'Finishing Position', 'y': 'Count'},title=f'Finishing Position Distribution for {selected_team}',  color_discrete_sequence=['#0000FF'] )

        

        col3,col4 = st.columns(2)

        with col3:

            st.plotly_chart(fig1,use_container_width= True)

        with col4:

            st.plotly_chart(fig2,use_container_width=True )



drivers_df['full_name']=drivers_df['forename'] + ' ' +drivers_df['surname' ]

#track layout and length from wikipedia
def get_track_info(wiki_url):

    if not isinstance(wiki_url,str) or not wiki_url.startswith("http" ):

        return None,None  #return nothing for both

    try:

        response= requests.get(wiki_url)

        if response.status_code!= 200:
            return None, None


        soup= BeautifulSoup(response.text,'html.parser')

        infobox =soup.find('table', {'class': 'infobox'})


        track_length= None
        track_image_url =None

        if infobox:

            img_tags= infobox.find_all('img')

            #try find layout of track
            for img in img_tags:

                img_url = "https:" + img['src']

                if ("circuit" in img_url.lower() or "layout" in img_url.lower()) and "map" not in img_url.lower():    

                    track_image_url =img_url

                    break  #stop once image found




            #get length from infobox
            for row in infobox.find_all('tr' ):

                header1 =row.find('th')
                data =row.find('td')
                if header1 and data:

                    if "length" in header1.text.lower():

                        track_length=data.text.strip()
                        track_length =re.sub(r"\[.*?\]", "",track_length ) 

                        break  



    except Exception as e:
        return None, None #silent error handling

    return track_image_url,track_length



#show location on map with red pin
def show_track_location(selected_track):

    track_row =tracks_df[tracks_df['name'] ==selected_track].iloc[0 ]

    
    #coordinates
    latitude = track_row['lat']
    longitude = track_row['lng']

    #check for coordinate available
    if pd.isna(latitude) or pd.isna(longitude ):

        st.write("No GPS coordinates available for this track. " )

        return

    #creaet map
    fig= go.Figure()

    #marker
    fig.add_trace(go.Scattermapbox(lat =[latitude],lon=[longitude],mode='markers',marker= go.scattermapbox.Marker(size=29, color='red' ),text=selected_track, hoverinfo="text"))



    #map layout
    fig.update_layout(
        mapbox=dict(

            style="open-street-map",
            zoom=12,  #zoom level
            center={"lat": latitude, "lon": longitude}

        ),

        title= f"Location of {selected_track}" 

    )
    st.plotly_chart(fig, use_container_width=True)

#Tracks PG
def tracks():

    st.markdown("<p class='stTitle'>Track Information</p>",unsafe_allow_html= True )

    st.write("Explore Formula 1 circuits and track statistics.")

    #track dropdown
    selected_track= st.sidebar.selectbox('Select a Track',tracks_df['name'].unique(),index= 0)

    track_row = tracks_df[tracks_df['name'] == selected_track].iloc[0]

    #wiki fetch
    wikiUrl =track_row.get('url', None)

    track_image_url,track_length =get_track_info(wikiUrl) if wikiUrl else (None,None)

    #filter
    track_races =races_df[races_df['circuitid'] ==track_row['circuitid'] ]

    num_races =track_races.shape[0]


    track_results =results_df[results_df['raceid'].isin(track_races['raceid'])]

    if not track_results.empty and 'fastestlap' in track_results.columns: 

        fastest_lap_row=track_results.loc[track_results['fastestlap'].idxmin() ] #row with fastest lap

        fastest_lap =fastest_lap_row['fastestlap']

        fastest_driver_id= fastest_lap_row['driverid' ]

        fastest_driver=(
            drivers_df.loc[drivers_df['driverid'] == fastest_driver_id, 'full_name'].values[0 ]

            if fastest_driver_id and not drivers_df[drivers_df['driverid'] == fastest_driver_id].empty

            else "NA"

        )

    else:
        fastest_lap ="NA"

        fastest_driver = "NA"



    col1,col2 =st.columns([1,2] )

    with col1:

        if track_image_url and track_image_url.startswith("https://upload.wikimedia.org/"):

            st.image(track_image_url,caption=selected_track,width=500)

        else:

            st.write("No image available for this track." )

    with col2:
        st.markdown(f"<p class='driver-info'><span class='highlight'>Track Name:</span>{track_row['name']}</p>",unsafe_allow_html=True )

        st.markdown(f"<p class='driver-info'><span class='highlight'>Location:</span>{track_row['location']},{track_row['country']}</p>",unsafe_allow_html=True )

        if track_length:
            st.markdown(f"<p class='driver-info'><span class='highlight'>Track Length:</span>{track_length}</p>",unsafe_allow_html=True) 

        st.markdown(f"<p class='driver-info'><span class='highlight'>Number of Races Held:</span>{num_races}</p>",unsafe_allow_html=True  )

        if fastest_lap!="NA":

            st.markdown(f"<p class='driver-info'><span class='highlight'>Fastest Lap:{fastest_driver}</p>", unsafe_allow_html=True )
        
    show_track_location(selected_track)




#Simulated Races PG
def simulated_races():

    st.markdown("<p class='stTitle'>Simulated Races</p>", unsafe_allow_html=True)
    st.write("Simulated race outcomes based on historical data.")

    st.markdown("""
        <p style= "font-size:44px; font-weight:bold; text-align:center;">
        Under Construction
        </p>
        <p>    </p>
        <p>    </p>
        <p style="font-size:44px; font-weight:bold; text-align:center;">
        coming <span style="color:red;">soon</span>  </p>
    """, unsafe_allow_html=True)

#routing
if choice=='Home':
    home()
    
elif choice== 'Driver Info':
    driver_info()

elif choice =='Team Info':
    team_info()

elif choice=='Tracks':
    tracks()



elif choice=='Simulated Races':
    simulated_races()

