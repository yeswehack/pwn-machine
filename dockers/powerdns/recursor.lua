protobufServer("127.0.0.1:4000", {
    logQueries = true,
    logResponses = true,
    exportTypes = {'A', 'AAAA', 'CNAME', 'MX', 'PTR', 'NS', 'SPF', 'SRV', 'TXT'}
})
addNTA(".")
--[[ outgoingProtobufServer("127.0.0.1:4000", {
    logQueries = true,
    logResponses = true,
    exportTypes = {'A', 'AAAA', 'CNAME', 'MX', 'PTR', 'NS', 'SPF', 'SRV', 'TXT'}
}) ]]
