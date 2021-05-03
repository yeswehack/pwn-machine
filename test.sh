http delete http://127.0.0.1:8081/api/v1/servers/localhost/zones/test.com 'X-API-KEY: test' 
# http delete http://127.0.0.1:8081/api/v1/servers/localhost/zones/pouet.com 'X-API-KEY: test' 
# http post http://127.0.0.1:8081/api/v1/servers/localhost/zones 'X-API-KEY: test' \
#      name=test.com. \
#      kind=native  \
#      nameservers:='["ns.test.com."]' \
#      'soa_edit=INCEPTION-EPOCH' \
#      'soa_edit_api=INCEPTION-EPOCH' 

# http patch http://127.0.0.1:8081/api/v1/servers/localhost/zones/test.com. 'X-API-KEY: test' \
#      'rrsets:=[{"name": "test.test.com.", "ttl": 10, "type":"A", "changetype": "REPLACE", "records": [{"content": "127.0.0.1", "disabled": false}] }]'

# http patch http://127.0.0.1:8081/api/v1/servers/localhost/zones/bi.tk 'X-API-KEY: test' \
#      'rrsets:=[{"name": "bi.tk.", "type":"SOA", "changetype": "REPLACE", "ttl": 3660, "records": [{"content": "ns.bi.tk. postmaster.bi.tk. 2021030203 10800 3600 604800 3600", "disabled": false }] }]'
