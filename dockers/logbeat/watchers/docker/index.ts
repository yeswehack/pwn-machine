import moment from "moment";
import { Database } from "sqlite3";
import { promisify } from "util";
import type { ILogfileWatcher } from "../../types/ILogfileWatcher";
import { promisifyStatement } from "../../utils";

const escape = (s: string) => s.replace(/'/g, "''");

function get_insert_query(image: string, container: string): string {
  return `
  INSERT INTO docker_logs (date, image, container, stream, log)
  VALUES  (?, '${escape(image)}', '${escape(container)}', ?, ?);
  `;
}

const SELECT_LAST_LOG_DATE = `SELECT max(date) as date FROM docker_logs WHERE container = ? AND image = ?;`;

function parseLog(log: string) {
  const j = JSON.parse(log);
  return {
    date: moment(j["time"]).unix(),
    log: j["log"],
    stream: j["stream"],
  };
}

export default class DockerLogfileWatcher implements ILogfileWatcher {
  insert!: (...x: any[]) => Promise<void>;
  lastLogDate!: number;

  constructor(public image: string, public container: string) {}

  async setup(db: Database) {
    // Prepare this.insert
    const query = get_insert_query(this.image, this.container);
    this.insert = promisifyStatement(db, query);

    // Select last log date
    const selectOne = promisify(db.get.bind(db)) as (
      query: string,
      args: [string, string]
    ) => Promise<{ date: number } | null>;
    const row = await selectOne(SELECT_LAST_LOG_DATE, [
      this.container,
      this.image,
    ]);
    this.lastLogDate = row?.date ?? 0;
    return this;
  }

  async handleLine(line: string): Promise<void> {
    const log = parseLog(line);
    if (log.date > this.lastLogDate) {
      await this.insert(log.date, log.stream, log.log);
    }
  }
}
