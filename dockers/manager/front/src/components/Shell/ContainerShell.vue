<template>
  <div class="terminal-container">
    <div ref="terminal" class="terminal">
      <q-resize-observer @resize="onResize" :debounce="300" />
    </div>
    <q-btn
      v-if="started"
      class="poweroff"
      round
      icon="power_settings_new"
      size="sm"
      color="negative"
      @click="exit"
    />
  </div>
</template>

<script>
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { WebLinksAddon } from "xterm-addon-web-links";

const WS_URL = `ws://127.0.0.1:8000/shell`;

function openWS(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    ws.addEventListener("open", () => resolve(ws));
    ws.addEventListener("error", e => reject(e));
  });
}

function waitForSocketClose(ws) {
  return new Promise(resolve => {
    ws.addEventListener("close", () => {
      resolve();
    });
  });
}

async function closeSocket(ws) {
  const p = waitForSocketClose(ws);
  ws.close();
  return await p;
}

class Shell {
  constructor() {
    this.started = false;
    this.fitAddon = new FitAddon();
    this.webLinksAddon = new WebLinksAddon();
    this.term = new Terminal({
      cursorBlink: true,
      scrollback: 1000
    });
    this.term.loadAddon(this.fitAddon);
    this.term.loadAddon(this.webLinksAddon);
    this.term.onData(data => this.onLocalData(data));
  }

  async start(el, url) {
    return new Promise((resolve, reject) => {
      openWS(url)
        .then(ws => {
          this.ws = ws;
          this.ws.addEventListener("message", evt => {
            this.onRemoteData(evt.data);
          });
          this.ws.addEventListener("close", () => {
            this.term.blur();
            this.started = false;
            resolve();
          });
          this.term.open(el);
          this.term.focus();
          this.started = true;
          this.fit();
        })
        .catch(e => {
          reject(e);
        });
    });
  }

  async stop() {
    if (!this.ws) return;
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
      case WebSocket.OPEN:
        await closeSocket(this.ws);
        break;
      case WebSocket.CLOSING:
        await waitForSocketClose(this.ws);
        break;
      case WebSocket.CLOSED:
        break;
    }
  }

  onRemoteData(data) {
    const msg = JSON.parse(data);
    if ("stdout" in msg) {
      this.term.write(msg.stdout);
    }
    if ("exit" in msg) {
      this.ws.close();
    }
  }

  send(data) {
    this.ws.send(JSON.stringify(data));
  }

  onLocalData(data) {
    this.send({ stdin: data });
  }

  exit() {
    this.send({ exit: true });
  }

  fit() {
    if (!this.started) return;
    this.fitAddon.fit();
    const resize = {
      cols: this.term.cols,
      rows: this.term.rows
    };
    this.send({ resize });
  }
}

export default {
  props: {
    uuid: { type: String, required: true }
  },
  data() {
    const shell = new Shell();
    return { shell };
  },
  methods: {
    onResize(size) {
      this.shell.fit();
    },
    exit() {
      this.shell.exit();
    },
    disconnect() {
      return this.shell.stop();
    },
    connect() {
      this.shell
        .start(this.$refs.terminal, WS_URL + "/" + this.uuid)
        .then(() => {
          this.$q.notify({
            message: "Connection closed",
            color: "negative",
            position: "top"
          });
        })
        .catch(e => {
          this.$router.push({ name: "shellNew" });
        });
    }
  },
  computed: {
    started() {
      return this.shell?.started ?? false;
    }
  },
  mounted() {
    this.connect();
  },
  watch: {
    $route: {
      immediate: true,
      async handler() {
        //await this.disconnect();
        //this.connect();
      }
    }
  }
};
</script>

<style>
@import "~xterm/css/xterm.css";
.terminal {
  flex-grow: 1;
  height: 100%;
  width: 100%;
}

.terminal-container {
  flex-grow: 1;
  height: 100%;
  width: 100%;
  position: relative;
}

.poweroff {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 100;
}
</style>
