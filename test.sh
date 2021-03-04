http delete http://127.0.0.1:8081/api/v1/servers/localhost/zones/bi.tk 'X-API-KEY: test' 
http delete http://127.0.0.1:8081/api/v1/servers/localhost/zones/pouet.com 'X-API-KEY: test' 
http post http://127.0.0.1:8081/api/v1/servers/localhost/zones 'X-API-KEY: test' \
     id=bi.tk \
     name=bi.tk. \
     kind=Native  \
     nameservers:='["ns.bi.tk."]' \
     'soa-edit=INCEPTION-INCREMENT' 

http patch http://127.0.0.1:8081/api/v1/servers/localhost/zones/bi.tk 'X-API-KEY: test' \
     'rrsets:=[{"name": "test.bi.tk.", "type":"A", "changetype": "REPLACE", "ttl": 60, "records": [{"content": "127.0.0.1", "disabled": false}] }]'

http patch http://127.0.0.1:8081/api/v1/servers/localhost/zones/bi.tk 'X-API-KEY: test' \
     'rrsets:=[{"name": "bi.tk.", "type":"SOA", "changetype": "REPLACE", "ttl": 3660, "records": [{"content": "ns.bi.tk. postmaster.bi.tk. 2021030203 10800 3600 604800 3600", "disabled": false }] }]'
