'''
The network mixin provides:

    client_ip -- the IP number of the computer where the
                 browser is 
                 (be aware that this can be faked)
    me() -- return True iff request is from 127.0.0.1
    us() -- return True iff localServe is an IP number
                   of the same 24/8 network as the request
            # the idea here was to allow service to local 
            # service only when localServe is set to a
            # the IP of a network's gateway -- however this
            # works only for some hardwired local networks
            # (i.e. not for wifi's) and is not documented 
            # elsewhere
    serve() -- return True iff 
                        me() and localServe==True ()
                        localServe==False
                        us() and localServe not boolean
'''

def getResources():

    return dict ( 
        client_ip = handler.client_address[0],
        me = lambda: _me(handler), 
        us = lambda: _us(handler), 
        serve = lambda: _serve(handler)
    )

def _me(handler):
    return handler.client_address[0]=='127.0.0.1'
           # this one IP number isn't going to be faked
    
def _us(handler):
    import os
    co = unmixed('constants')
    ha = co.client_iphandler.client_address[0]
     # only works for subnet 255.255.255.0 networks
     # with one gateway
    a,b = os.path.splitext(co.localServe)
    x,y = os.path.splitext(ha)
    return (ha=='127.0.0.1' or (a==x and b!=y) )

def _serve(handler):
    co = unmixed('constants')
    if isinstance(co.localServe,bool):
       #print "bool and returning " + str(
       #           (not co.localServe) or _me(handler))
       return (not co.localServe) or _me(handler)
    else:
       #print "ip and returning " + str(_us(handler))
       return _us(handler)
    
   
