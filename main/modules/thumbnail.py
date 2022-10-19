import asyncio
from config import CHANNEL_TITLE
import os
import random, cv2
from string import ascii_uppercase, digits
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup as bs
from .utils import get_screenshot

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""
    pos = 0    
    for i in list:
        if len(text1) + len(i) < 16 and pos == 0:        
            text1 += " " + i
        elif len(text2) + len(i) < 16:
            pos = 1       
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return text1,text2

err = 0

async def get_cover(id):
    global err
    
    try:
        url = 'https://graphql.anilist.co'
        anime_query = '''
   query ($id: Int,$page: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
            month
            day
          }
        endDate{
            year
            month
            day
            }
          episodes
          isLicensed
          recommendations(page:$page, perPage:8, sort:RATING_DESC,){
            pageInfo {
                lastPage
                total}
            edges{
                node{
                    mediaRecommendation{title{romaji}
                    coverImage{
              extraLarge}
              siteUrl
              averageScore
                    id}
                    rating
                }}
          }
          isAdult
          popularity
          source
          externalLinks{
              type
              url
              site
              language
              icon
              isDisabled
              }
          season
          type
          format
          status
          countryOfOrigin
          duration
          hashtag
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          nextAiringEpisode {
              timeUntilAiring
              episode
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          synonyms
          relations{
            edges{
                relationType
                node{
                    title{romaji}}
                    }
          }
          bannerImage
          coverImage{
              extraLarge}
          characters(page: $page, perPage: 25,sort:ROLE){
                pageInfo {
                    lastPage
                    total
              }
              edges{
                  node{
                    name{full}
                      }
                  role
                  }
                }
                  
      }
    }
'''
        variables = {'id':id}        
        json = requests.post(url,json={
                'query': anime_query,
            'variables': variables}).json()
        json = json['data']['Media']
        cover = json['coverImage']['extraLarge']
        r = requests.get(cover).content

        fname = "./" + "".join(random.choices(ascii_uppercase + digits,k = 10)) + ".jpg"
        with open(fname,"wb") as file:
            file = file.write(r)

        err = 0
        return fname
    except:
        await asyncio.sleep(2)

        err += 1
        if err != 5:
            return await get_cover(id)
        else:
            err = 0
            return "assets/c4UUTC4DAe.jpg"

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_thumbnail(id,file,title,ep_num,size,dur):
    ss = get_screenshot(file)
    cc = await get_cover(id)
    thumb = cc
    
    try:
        os.remove(ss)
        if cc != "assets/c4UUTC4DAe.jpg":
            print("lol")
    except:
        pass
    return thumb
