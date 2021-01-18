import requests
from .models import Thread
from .models import Post
import re

from django.core.files.base import ContentFile

def get_all_b_ylyl_threads():
    x = requests.get('https://a.4cdn.org/b/catalog.json')

    for page in x.json():   
        for thread in page['threads']:             
            if re.search(r'(yl yl)|(ylyl)', thread['com'], re.IGNORECASE):
                try:
                    thethread = Thread.objects.get(threadid=thread['no'])     

                    if thethread.active == True:
                        postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json') 
                        posts_online = thread['images']
                        print("thread : " + str(thread['no']) + "  images in db " + str(thethread.mediacount) + " new ones: " + str(posts_online) + " " + str(postlist.status_code))  
                                               

                        if str(postlist.status_code) == '404':
                            print(str(thread['no']) + " inactive")
                            thethread.active = False
                            thethread.save()
                        else:  

                            thethread.mediacount = posts_online
                            thethread.save()

                            for post in postlist.json()['posts']:
                                # print("post : " + str(post['no']) + ' -------------------- ')
                                try:
                                    newpost = Post(postid=post['no'], thread=thethread)
                                    newpost.ext = post['ext']
                                    newpost.tim = post['tim']
                                    newpost.save()
                                    # print("ext " + post['ext'])
                                    # print("tim " + str(post['tim']))
                                except:
                                    pass

                except Thread.DoesNotExist:
                    # print(str(thread['no']) + " DoesNotexist")
                    newthread = Thread(threadid=thread['no'], summary=thread['com'], mediacount=thread['images'])
                    newthread.active = True
                    newthread.save()
                        
                    postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json')  

                    if str(postlist.status_code) == '404':
                        print(str(thread['no']) + " inactive")
                        newthread.active = False
                        newthread.save()
                    else:            
                        for post in postlist.json()['posts']:
                            try:
                                newpost = Post(postid=post['no'], thread=newthread)
                                newpost.ext = post['ext']
                                newpost.tim = post['tim']
                                newpost.save()
                            except:
                                # IF this is not a media post
                                pass

    
    query = Thread.objects.all()    
    for thread in query:
        print("===========")
        print(str(thread.threadid) + " Active : " + str(thread.active) + " count: " + str(thread.mediacount) + " " + thread.summary)
        
        # check thread and delete if inactive

        postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread.threadid) + '.json') 

        if str(postlist.status_code) == '404':
            thread.delete()
        else:        
            getallposts = Post.objects.filter(thread=thread)    
            for post in getallposts:
                if post.fetched == False:
                    download_media(post, str(post.tim), post.ext)



def get_all_gif_ylyl_threads():

    return None

# def filter_threads():
#     query = Thread.objects.all()    
#     for thread in query:
#         print("===========")
#         print(str(thread.threadid) + " Active : " + str(thread.active) + " count: " + str(thread.mediacount) + " " + thread.summary)
#         getallposts = Post.objects.filter(thread=thread)    
#         for post in getallposts:
#             if post.fetched == False:
#                 download_media(post, str(post.tim), post.ext)

def download_media(post, file, extension):
    
    media = requests.get('https://i.4cdn.org/b/' + file + extension)  

    if str(media.status_code) == '200':
        post.mediafile = ContentFile(media.content, name=file+extension)
        post.fetched = True
        post.save()
        print(post.tim + post.ext + " SAVED")
    else:
        post.fetched == False
        post.save()
     
    return


# def get_all_ylyl_threads():

#     x = requests.get('https://a.4cdn.org/b/catalog.json')
#     for page in x.json():   
#         for thread in page['threads']:     

#             if re.search(r'(yl yl)|(ylyl)', thread['com']):
                
#                 print(thread['com'])

#             # try:
#             #     thethread = Thread.objects.get(threadid=thread['no']) 


#             posts_online = thread['images']
#             print("thread : " + str(thread['no']) + "  images in db new ones: " + str(posts_online))