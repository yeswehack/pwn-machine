{% set SERIAL = pm_time().strftime("%Y%m%d%S") %}
{% for domain, ip in parse_json(PM_DOMAINS).items() %}

INSERT INTO
  domains (name, type)
SELECT
  '{{domain}}', 'NATIVE'
WHERE NOT EXISTS (
  SELECT * FROM domains WHERE name='{{domain}}'
);

INSERT IGNORE INTO
  records (domain_id, name, type, content, ttl, prio, disabled)
SELECT
  id ,'{{domain}}', 'SOA', 'ns.{{domain}} postmaster.{{domain}}  {{SERIAL}} 28800 1800 2419200 28800', 43200, 0, 0
FROM domains
WHERE
  name='{{domain}}'
AND NOT EXISTS (
  SELECT * FROM records WHERE name='{{domain}}' AND type="SOA"
);


INSERT INTO
  records (domain_id, name, type, content, ttl, prio, disabled)
SELECT
  id ,'{{domain}}', 'NS', 'ns.{{domain}}', 43200, 0, 0
FROM domains
WHERE name='{{domain}}'
AND NOT EXISTS (
  SELECT * FROM records WHERE name='{{domain}}' AND content="ns.{{domain}}" AND type="NS"
);


INSERT INTO
  records (domain_id, name, type, content, ttl, prio, disabled)
SELECT id ,'{{domain}}', 'A', '{{ip}}', 43200, 0, 0
FROM domains
WHERE name='{{domain}}'
AND NOT EXISTS (
  SELECT * FROM records WHERE name='{{domain}}' AND content="{{ip}}" AND type="A"
);


INSERT INTO
  records (domain_id, name, type,content,ttl,prio,disabled)
SELECT
  id ,'ns.{{domain}}', 'A', '{{ip}}', 43200, 0, 0
FROM domains
WHERE name='{{domain}}'
AND NOT EXISTS (
  SELECT * FROM records WHERE name='ns.{{domain}}' AND content="{{ip}}" AND type="A"
);


INSERT INTO
  records (domain_id, name, type, content, ttl, prio, disabled)
SELECT
  id ,'*.{{domain}}', 'CNAME', '{{domain}}', 43200, 0, 0
FROM domains
WHERE name='{{domain}}'
AND NOT EXISTS (
  SELECT * FROM records WHERE name='*.{{domain}}' AND content="{{domain}}" AND type="CNAME"
);


{% endfor %}
