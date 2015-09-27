def getResources(handler):
   cs = handler.server.soconsts
   return dict (
       getList = cs.getList,
       postList = cs.postList,
       appDirs = cs.appDirs
       )



