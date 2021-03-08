-- Remove expired key reference for all dns logs

local function read_all(k)
    local len = redis.call("ZCOUNT", k, "-inf", "+inf");
    return redis.call("ZRANGE", k, 0, len);
end

local domains_key = "dns/logs/domains"; 
local domains  = read_all(domains_key); -- list of domain keys
local total_deleted = 0;
for idx, domain_log in ipairs(domains) do
    local log_entries = read_all(domain_log); -- list of log key for domain
    local deleted = 0;
    for idx, log_enty in ipairs(log_entries) do 
        -- if log entry is expired, remove from set
        local exists = redis.call("EXISTS", log_enty);
        if exists == 0 then
           redis.call("ZREM", domain_log, log_enty);
           deleted = deleted + 1;
        end
    end

    if deleted > 0 and deleted == #log_entries then
        -- if all entries are deleted, remove from domain list
        redis.call("ZREM", domains_key, domain_log);
    end
    total_deleted = total_deleted + deleted;
end

return total_deleted;
