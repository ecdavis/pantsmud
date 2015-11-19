SpaceGame
=========

Server
------

    > python mud.py

Client
------

    > telnet localhost 4040
    > register
    register.success {"uuid": "287708fc-4ef6-4887-9b22-00b84f2142e5"}
    > login 287708fc-4ef6-4887-9b22-00b84f2142e5
    login.success
    scan {"node": "example", "mobiles": ["f8211ccb-25d9-4b0b-bac0-580a2972601a"], "links": ["example"]}
    > broadcast.local hello
    broadcast.local {"mobile_from": "f8211ccb-25d9-4b0b-bac0-580a2972601a", "message": "hello"}
    > broadcast.global hello
    broadcast.global {"mobile_from": "f8211ccb-25d9-4b0b-bac0-580a2972601a", "message": "hello"}
    > broadcast.private f8211ccb-25d9-4b0b-bac0-580a2972601a hello
    broadcast.private {"mobile_from": "f8211ccb-25d9-4b0b-bac0-580a2972601a", "message": "hello", "mobile_to": "f8211ccb-25d9-4b0b-bac0-580a2972601a"}
    broadcast.private {"mobile_from": "f8211ccb-25d9-4b0b-bac0-580a2972601a", "message": "hello", "mobile_to": "f8211ccb-25d9-4b0b-bac0-580a2972601a"}
    > scan
    scan {"node": "example", "mobiles": ["f8211ccb-25d9-4b0b-bac0-580a2972601a"], "links": ["example"]}
    > jump example
    scan {"node": "other_example", "mobiles": ["f8211ccb-25d9-4b0b-bac0-580a2972601a"], "links": []}
    jump.success
    > who.list
    who.list {"mobiles": ["f8211ccb-25d9-4b0b-bac0-580a2972601a"]}
    > shutdown
