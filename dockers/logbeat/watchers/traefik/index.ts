import moment from "moment";
import { Database } from "sqlite3";
import { promisify } from "util";
import type { ILogfileWatcher } from "../../types/ILogfileWatcher";
import { promisifyStatement } from "../../utils";

const INSERT_LOG = `INSERT INTO traefik_logs 
(date, origin, status, host, method, path, port, protocol, scheme, router_name, entrypoint_name, service_name)
VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);`;

const SELECT_LAST_LOG_DATE = `SELECT max(date) as date FROM traefik_logs;`;

function parseLog(log: string) {
  
  const j = JSON.parse(log);
  const router_name = j["RouterName"];
  return {
    date: moment(j["time"]).unix(),
    origin: j["ClientHost"],
    status: j["DownstreamStatus"],
    host: j["RequestHost"],
    method: j["RequestMethod"],
    path: j["RequestPath"],
    port: j["RequestPort"],
    protocol: j["RequestProtocol"],
    scheme: j["RequestScheme"],
    entrypoint_name: j["entryPointName"],
    router_name,
    service_name:
      router_name == "api@internal" ? "api@internal" : j["ServiceName"],
  };
}

export default class PowerdnsLogfileWatcher implements ILogfileWatcher {
  insert!: (...x: any[]) => Promise<void>;
  lastLogDate!: number;

  async setup(db: Database) {
    // Select last log date
    const selectOne = promisify(db.get.bind(db)) as (
      query: string
    ) => Promise<{ date: number } | null>;
    const row = await selectOne(SELECT_LAST_LOG_DATE);
    this.lastLogDate = row?.date ?? 0;

    // Prepare insert
    this.insert = promisifyStatement(db, INSERT_LOG);
    return this;
  }

  async handleLine(line: string): Promise<void> {
    const log = parseLog(line);
    if (log && log.date > this.lastLogDate) {
      await this.insert(
        log.date,
        log.origin,
        log.status,
        log.host,
        log.method,
        log.path,
        log.port,
        log.protocol,
        log.scheme,
        log.router_name,
        log.entrypoint_name,
        log.service_name
      );
      this.lastLogDate = log.date;
    }
  }
}
