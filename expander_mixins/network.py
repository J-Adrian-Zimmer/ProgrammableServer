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
        me = _me, 
        us = _us, 
        serve = _serve
    )

def _me():
    return handler.client_address[0]=='127.0.0.1'
           # this one IP number isn't going to be faked
    
def _us():
    import os
    co = unmixed('constants')
    ha = co.client_iphandler.client_address[0]
     # only works for subnet 255.255.255.0 networks
     # with one gateway
    a,b = os.path.splitext(co.localServe)
    x,y = os.path.splitext(ha)
    return (ha=='127.0.0.1' or (a==x and b!=y) )

def _serve():
    co = unmixed('constants')
    if isinstance(co.localServe,bool):
       return (not co.localServe) or _me()
    else:
       return _us()
    
   
