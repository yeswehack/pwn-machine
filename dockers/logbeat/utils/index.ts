import { Database } from "sqlite3";
import { promisify } from "util";

export function promisifyStatement(db: Database, statement: string) {
  const insertStatement = db.prepare(statement);
  const runInsertStatement = promisify(
    insertStatement.run.bind(insertStatement)
  ) as (arg0: any[]) => Promise<void>;
  return (...x: any[]) => runInsertStatement(x);
}