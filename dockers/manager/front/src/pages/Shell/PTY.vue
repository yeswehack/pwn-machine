<template>
  <div ref="terminal" class="terminal"></div>
</template>

<script>
import io from "socket.io-client";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { WebLinksAddon } from "xterm-addon-web-links";
import { SearchAddon } from "xterm-addon-search";


function debounce(func, wait_ms = 50) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait_ms);
  };
}
export default {
  props: {
    uuid: String,
  },
  data() {
    const fitAddon = new FitAddon();
    const webLinksAddon = new WebLinksAddon();
    const searchAddon = new SearchAddon();
    const term = new Terminal({
      cursorBlink: true,
      scrollback: 1000,
    });
    term.loadAddon(fitAddon);
    term.loadAddon(webLinksAddon);
    term.loadAddon(searchAddon);
    term.onData((data) => this.onData(data));
    return { term, fitAddon, searchAddon };
  },
  methods: {
    onData(data) {
      this.socket.emit("pty_input", { uuid: this.uuid, input: data });
    },

    fit() {
      this.fitAddon.fit();
      this.socket.emit("resize", {
        uuid: this.uuid,
        cols: this.term.cols,
        rows: this.term.rows,
      });
    },
  },
  beforeDestroy() {
    this.socket.close();
  },
  mounted() {
    this.socket = new io(`ws://127.0.0.1:5000/shell`);
    this.term.open(this.$refs.terminal);
    this.term.focus();
    this.fit();
    window.onresize = debounce(() => this.fit());

    this.socket.on("pty_output", (data) => {
      this.term.write(data.output);
    });
    this.socket.on("shell_closed", (data) => {
      this.$emit("close")
    });
    this.socket.emit("attach", { uuid: this.uuid })
    this.socket.emit("get_logs", { uuid: this.uuid });
  },
};
</script>

<style>
@import "~xterm/css/xterm.css";
.terminal {
  flex-grow: 1;
  height: 100%;
}
</style>