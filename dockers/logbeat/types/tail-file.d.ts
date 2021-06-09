declare class Tail {
  constructor(filename, options: { force: boolean; startPos: number });
  on(event: string, callback: (string) => void);
  startP(): Promise<void>;
  stop(): Promise<void>;
}

declare module "tail-file" {
  export = Tail;
}
