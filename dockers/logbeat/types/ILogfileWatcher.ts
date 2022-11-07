import type { Database } from "sqlite3";

export interface ILogfileWatcher {
  handleLine(line: String): Promise<void>;
  setup(db: Database): Promise<ILogfileWatcher>;
}
