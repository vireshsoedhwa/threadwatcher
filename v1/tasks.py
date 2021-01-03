import requests
from .models import Thread
from .models import Post

from django.core.files.base import ContentFile

def get_all_threads():
    x = requests.get('https://a.4cdn.org/b/catalog.json')

        # logger.error(x.json())

    for page in x.json():   
        for thread in page['threads']: 
            # one_entry = Entry.objects.get(pk=1)
            
            try:
                thethread = Thread.objects.get(threadid=thread['no'])     

                if thethread.active == True:
                    postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json') 
                    print("thread : " + str(thread['no']) + " " + str(postlist.status_code))  
                    
                    if str(postlist.status_code) != '200':
                        print(str(thread['no']) + " inactive")
                        thethread.active = False
                        thethread.save()
                    else:            
                        for post in postlist.json()['posts']:
                            print("post : " + str(post['no']) + ' -------------------- ')
                            try:
                                newpost = Post(postid=post['no'], thread=newthread)
                                newpost.ext = post['ext']
                                newpost.tim = post['tim']
                                newpost.save()
                                print("ext " + post['ext'])
                                print("tim " + str(post['tim']))
                            except:
                                pass

            except Thread.DoesNotExist:
                # print(str(thread['no']) + " DoesNotexist")
                newthread = Thread(threadid=thread['no'], summary=thread['com'])
                newthread.active = True
                newthread.save()
                    
                postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json')  

                if str(postlist.status_code) != '200':
                    print(str(thread['no']) + " inactive")
                    newthread.active = False
                    newthread.save()
                else:            
                    for post in postlist.json()['posts']:
                        print("post : " + str(post['no']) + ' -------------------- ')
                        try:
                            newpost = Post(postid=post['no'], thread=newthread)
                            newpost.ext = post['ext']
                            newpost.tim = post['tim']
                            newpost.save()
                            print("ext " + post['ext'])
                            print("tim " + str(post['tim']))
                        except:
                            pass

                # for item in postlist.json():
                #     print(item)

                    # newpost = Post(postid=)
                
                # newpost = Post()

                # print(str(thread['no']) + " Added")

            # newthread = Thread(threadid=thread['no'], summary=thread['com'])
            # newthread.save()
            

    # for thread in Thread.objects.all()[:5]:
        
    #     try:
    #         postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread.threadid) + '.json')  

    #         for post in postlist.json()['posts']:
    #             print(post['no'])

    #     except:
    #         print('error')
    #         thread.delete()
    #         pass

def filter_threads():

    query = Thread.objects.filter(summary__iregex=r'(yl yl)|(ylyl)')
    
    for thread in query:
        print("===========")
        print("active " + str(thread.active))
        print(thread.threadid)
        print(thread.summary)

        getallposts = Post.objects.filter(thread=thread)
        
        print("Total posts: " + str(len(getallposts)))

        for post in getallposts:
            print(post.tim)
            print(post.ext)
            # media = requests.get('https://i.4cdn.org/b/' + str(post.tim) + str(post.ext))  

            if post.fetched == False:
                download_media(post, str(post.tim), post.ext)




            # post.mediafile = media.content
            # post.save()
            # https://i.4cdn.org/[board]/[4chan image ID].[file extension]

def download_media(post, file, extension):
    
    media = requests.get('https://i.4cdn.org/b/' + file + extension)  

    if str(media.status_code) == '200':
        post.mediafile = ContentFile(media.content, name=file+extension)
        post.fetched = True
        post.save()
    else:
        pass   
     
    return