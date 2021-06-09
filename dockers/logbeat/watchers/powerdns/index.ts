import moment from "moment";
import { Database } from "sqlite3";
import { promisify } from "util";
import { ILogfileWatcher } from "../../types/ILogfileWatcher";
import { promisifyStatement } from "../../utils";

const INSERT_LOG = `INSERT INTO powerdns_logs (date, origin, query, type) VALUES  (?, ?, ?, ?);`;

const SELECT_LAST_LOG_DATE = `SELECT max(date) as date FROM powerdns_logs;`;

function unescape(s: string) {
  function replacer(s: string) {
    return String.fromCharCode(parseInt(s.slice(1), 10));
  }
  return s.replace(/\\\d{3}/g, replacer);
}

const queryRegex =
  /.*?Remote (?<origin>\d+\.\d+\.\d+\.\d+) wants '(?<query>.+?)\|(?<type>[A-Z]+)', /;

function parseLog(log: string) {
  const date = moment(log.slice(0, 15), "MMMM DD hh:mm:ss").unix();
  const message = log.slice(15).split(":").slice(1).join(":").trim();
  const match = queryRegex.exec(message);
  if (!match || !match.groups) {
    return;
  }
  const groups = match.groups;
  return {
    date,
    origin: groups.origin,
    query: unescape(groups.query),
    type: groups.type,
  };
}

export default class PowerdnsLogfileWatcher implements ILogfileWatcher {
  insert!: (...x: [number, string, string, string]) => Promise<void>;
  lastLogDate!: number;

  async setup(db: Database) {
    // Select last log date
    const selectOne = promisify(db.get.bind(db)) as (
      query: string
    ) => Promise<{ date: number } | null>;
    const row = await selectOne(SELECT_LAST_LOG_DATE);
    this.lastLogDate = row?.date ?? 0;

    // prepare insert
    this.insert = promisifyStatement(db, INSERT_LOG);
    return this;
  }

  async handleLine(line: string): Promise<void> {
    const log = parseLog(line);
    if (!log) return;
    if (log.date > this.lastLogDate) {
      await this.insert(log.date, log.origin, log.query, log.type);
      this.lastLogDate = log.date;
    }
  }
}
