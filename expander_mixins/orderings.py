'''
The orderings mixin provides the lists from expanderOrderings.json
'''

def getResources():
   cs = handler.server.soconsts
   return dict (
       getList = cs.getList,
       postList = cs.postList,
       appDirs = cs.appDirs
       )



