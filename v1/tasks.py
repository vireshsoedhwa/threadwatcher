import requests
from .models import Thread
from .models import Post

def getthreads():
    x = requests.get('https://a.4cdn.org/b/catalog.json')

        # logger.error(x.json())

    for page in x.json():   
        for thread in page['threads']: 
            # print(thread['no'])
            # one_entry = Entry.objects.get(pk=1)
            try:
                thethread = Thread.objects.get(threadid=thread['no'])     

                postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json') 
                print(str(thread['no']) + " " + str(postlist.status_code))   

                if str(postlist.status_code) != '200':
                    print(str(thread['no']) + " inactive")
                    thethread.active = False
                    thethread.save()

            except Thread.DoesNotExist:
                # print(str(thread['no']) + " DoesNotexist")
                newthread = Thread(threadid=thread['no'], summary=thread['com'])
                newthread.active = True
                newthread.save()
                
                try:                

                    postlist = requests.get('https://a.4cdn.org/b/thread/' + str(thread['no']) + '.json')  
                
                    for post in postlist.json()['posts']:
                        # print(post['no'])
                        newpost = Post(postid=post['no'], thread=newthread)
                        newpost.ext = post['ext']
                        newpost.tim = post['tim']
                        newpost.save()

                except:
                    print('error')
                    newthread.active = False
                    newthread.save()
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

