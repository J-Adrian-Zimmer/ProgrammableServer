''' 
The config mixin provides some settings from config.py
'''

def getResources(handler):
   sc = handler.server.soconsts
   return dict(
      web_root = sc.web_root,
      server_dir = sc.server_dir,
      localServe = sc.localServe,
      multithreading = sc.multithreading,
      unwanted_chars = sc.unwanted_chars
    )
