import { Database } from "sqlite3";
import { promisify } from "util";

const migrations = [`
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS docker_logs(
  date int,
  image text,
  container text,
  stream text,
  log text
);
CREATE INDEX IF NOT EXISTS docker_logs_stream ON docker_logs(stream); 
CREATE INDEX IF NOT EXISTS docker_logs_container ON docker_logs(container); 
CREATE INDEX IF NOT EXISTS docker_logs_image ON docker_logs(image); 


CREATE TABLE IF NOT EXISTS traefik_logs(
  date int,
  origin text,
  status int,
  host text,
  method text,
  path text,
  port int,
  protocol text,
  scheme text,
  router_name text,
  entrypoint_name text,
  service_name text
);
CREATE INDEX IF NOT EXISTS traefik_logs_router_name ON traefik_logs(router_name); 
CREATE INDEX IF NOT EXISTS traefik_logs_entrypoint_name ON traefik_logs(entrypoint_name); 
CREATE INDEX IF NOT EXISTS traefik_logs_service_name ON traefik_logs(service_name); 


CREATE TABLE IF NOT EXISTS powerdns_logs(
  date int,
  origin text,
  query text,
  type text
);
CREATE INDEX IF NOT EXISTS powerdns_logs_type ON powerdns_logs(type);
`];

export async function setup(db: Database) {
  const exec = promisify(db.exec.bind(db));
  for (const migration of migrations){
    await exec(migration)
  }
}
