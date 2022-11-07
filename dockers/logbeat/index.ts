import axios from "axios";
import * as fs from "fs";
import * as path from "path";
import * as sqlite3 from "sqlite3";
import Tail from "tail-file";
import { setup } from "./setup";
import type { ILogfileWatcher } from "./types/ILogfileWatcher";
import {
  DockerLogfileWatcher,
  PowerdnsLogfileWatcher,
  TraefikLogfileWatcher,
} from "./watchers";

const CONTAINERS_PATH = "/var/lib/docker/containers";

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function startFileReader(filename: string, watcher: ILogfileWatcher, startPos: string = "start") {
  for (;;) {
    try {
      const tail = new Tail(path.resolve(filename), {
        force: true,
        startPos,
      });
      tail.on("line", async (line: string) => {
        try {
          await watcher.handleLine(line);
        } catch {}
      });
      await tail.startP();
      return { stop: () => tail.stop() };
    } catch (e) {
      await sleep(1000);
    }
  }
}

type DockerEvent = {
  status: string;
  id: string;
  from: string;
  Type: string;
  Action: string;
  Actor: {
    ID: string;
    Attributes: { image: string; name: string };
  };
  scope: string;
  time: number;
  timeNano: number;
};

type CreatedContainer = {
  id: string;
  filename: string;
  image: string;
  container: string;
};

function* listAlreadyCreatedDocker(): Generator<CreatedContainer> {
  const containerIds = fs.readdirSync(CONTAINERS_PATH);
  for (const id of containerIds) {
    try {
      const configStr = fs.readFileSync(
        `${CONTAINERS_PATH}/${id}/config.v2.json`,
        { encoding: "utf-8" }
      );
      const config = JSON.parse(configStr);
      if ("Config" in config && "Image" in config.Config && "Name" in config) {
        const filename = `${CONTAINERS_PATH}/${id}/${id}-json.log`;
        yield {
          id,
          filename,
          image: config.Config.Image,
          container: config.Name.replace(/^\/+(.*)/, "$1"),
        };
      }
    } catch {
      continue;
    }
  }
}

async function startDockerEventListener(db: sqlite3.Database) {
  const watchers = new Map();
  for (const info of listAlreadyCreatedDocker()) {
    const watcher = await new DockerLogfileWatcher(
      info.image,
      info.container
    ).setup(db);
    const { stop } = await startFileReader(info.filename, watcher);
    watchers.set(info.id, stop);
  }

  const filters = {
    type: ["container"],
    event: ["create", "destroy"],
  };
  const search = new URLSearchParams({ filters: JSON.stringify(filters) });
  const url = `http:///v1.40/events?${search}`;

  const { data } = await axios({
    url,
    socketPath: "/var/run/docker.sock",
    responseType: "stream",
    timeout: 0,
  });

  data.on("data", async (chunk: Buffer) => {
    const event = JSON.parse(chunk.toString("utf-8")) as DockerEvent;
    const id = event.id;

    if (event.status === "create") {
      if (watchers.has(event.id)) return;
      const filename = `${CONTAINERS_PATH}/${id}/${id}-json.log`;
      const attrs = event.Actor.Attributes;
      const watcher = await new DockerLogfileWatcher(
        attrs.image,
        attrs.name
      ).setup(db);

      const { stop } = await startFileReader(filename, watcher);
      watchers.set(id, stop);
    }
    if (event.status === "destroy") {
      if (watchers.has(id)) {
        const stop = watchers.get(id);
        watchers.delete(id);
        await stop();
      }
    }
  });
}

async function main() {
  const db = new sqlite3.Database("/logs/all/logs.db");
  await setup(db);
  startDockerEventListener(db);

  const pdns = await new PowerdnsLogfileWatcher().setup(db);

  startFileReader("/logs/pdns/pdns.log", pdns, "end");

  const traefik = await new TraefikLogfileWatcher().setup(db);
  startFileReader("/logs/traefik/traefik.json", traefik);
}
main();
