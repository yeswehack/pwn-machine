<template>
  <div class="terminal-container">
    <div ref="terminal" class="terminal">
      <q-resize-observer @resize="onResize" :debounce="300" />
    </div>
    <q-btn
      v-if="!connected"
      class="poweroff"
      round
      icon="eva-trash"
      size="sm"
      title="Remove"
      color="negative"
      @click="remove"
    />
  </div>
</template>

<script>
import api from "src/api";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { WebLinksAddon } from "xterm-addon-web-links";

const WS_URL = `${window.location.protocol == "https:" ? "wss" : "ws"}://${
  window.location.host
}/ws/shell`;

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
    this.connected = false;
    this.exitCode = null;
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

  get running() {
    return this.exitCode === null;
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
            this.connected = false;
            resolve();
          });
          this.term.open(el);
          this.term.focus();
          this.connected = true;
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
    if ("status" in msg) {
      this.exitCode = msg["exitCode"];
      this.ws.close();
    }
  }

  send(data) {
    this.ws.send(JSON.stringify(data));
  }

  onLocalData(stdin) {
    this.send({ stdin });
  }

  fit() {
    if (!this.connected) return;
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
    id: { type: String, required: true }
  },
  data() {
    const shell = new Shell();
    return { shell, disconnecting: false };
  },
  methods: {
    onResize(size) {
      this.shell.fit();
    },

    remove() {
      this.$apollo.mutate({
        mutation: api.docker.shells.DELETE_SHELL,
        variables: { id: this.id },
        refetchQueries: [{ query: api.docker.shells.LIST_SHELLS }]
      }).then(() => {
        this.$router.push({name: "shellNew"})
      });
    },
    disconnect() {
      this.disconnecting = true;
      return this.shell.stop();
    },
    connect() {
      this.shell
        .start(this.$refs.terminal, WS_URL + "/" + this.id)
        .then(() => {
          if (!this.disconnecting)
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
    connected() {
      return this.shell?.connected ?? false;
    }
  },
  mounted() {
    this.connect();
  },
  beforeDestroy() {
    this.disconnect();
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
