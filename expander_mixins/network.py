'''
The network mixin provides:

    me() -- return True iff request is from 127.0.0.1
    us() -- return True iff localServe is an IP number
                   of the same 24/8 network as the request
    serve() -- return True iff 
                        me() and localServe==True ()
                        localServe==False
                        us() and localServe not boolean
    Note: us assumes that your local network is 24/8 and
          has only one gateway
'''

def getResources():

    return dict ( 
        me = lambda: _me(handler), 
        us = lambda: _us(handler), 
        serve = lambda: _serve(handler)
    )

def _me(handler):
    return handler.client_address[0]=='127.0.0.1'
    
def _us(handler):
    import os
    so = handler.server.soconsts
    ha = handler.client_address[0]
     # only works for subnet 255.255.255.0 networks
     # with one gateway
    a,b = os.path.splitext(so.localServe)
    x,y = os.path.splitext(ha)
    return (ha=='127.0.0.1' or (a==x and b!=y) )

def _serve(handler):
    so = handler.server.soconsts
    if isinstance(so.localServe,bool):
       #print "bool and returning " + str(
       #           (not so.localServe) or _me(handler))
       return (not so.localServe) or _me(handler)
    else:
       #print "ip and returning " + str(_us(handler))
       return _us(handler)
    
   
