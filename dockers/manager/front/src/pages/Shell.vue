<template>
  <TabPage :tab="tab" pathTemplate="/shell/{}">
    <template #top>
      <q-tab name="new" icon="add" class="bg-positive text-white" />
      <q-tab
        :name="uuid"
        :key="uuid"
        :label="name"
        v-for="{ name, uuid } of shells"
      />
      <q-space />
    </template>
    <template #tabs>
      <q-tab-panel name="new">
        <CreateShell/>
      </q-tab-panel>
      <q-tab-panel
        :name="uuid"
        :key="uuid"
        v-for="[idx, { uuid }] of shells.entries()"
      >
        <PTY :uuid="uuid" v-on:close="close(idx)" />
      </q-tab-panel>
    </template>
  </TabPage>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import PTY from "./Shell/PTY.vue";
import CreateShell from "src/components/Shell/Create.vue"

export default {
  // name: 'PageName',
  components: { TabPage, PTY, CreateShell },
  props: {
    tab: String
  },
  data() {
    return {
      shell: "",
      shells: []
    };
  },
  methods: {
    async fetchData() {
      this.shells = await this.$api.shell.getShells();
    },
    async createShell() {
      const name = "Host";
      const uuid = await this.$api.shell.createHostShell(name);
      this.shells.push({ name, uuid });
      this.show(uuid);
    },
    show(uuid) {
      this.$router.push({ name: "shell", params: { tab: uuid } });
    },
    close(idx) {
      this.shells.splice(idx, 1);
      if (this.shells.length) {
        this.show(this.shells[this.shells.length - 1].uuid);
      } else {
        this.show();
      }
    },
    init() {
      if (!this.tab) {
        if (!this.shells.length) {
          this.$router.push({ name: "shell", params: { tab: "new" } });
        } else {
          this.show(this.shells[0].uuid);
        }
      } else {
        if (!this.tab == "new" && !this.shells.find(({ uuid }) => uuid == this.tab)) {
          this.$router.push({ name: "shell", params: { tab: "new" } });
        }
      }
    }
  },
  async mounted() {
    await this.fetchData();
    this.init();
  },
  watch: {
    $route() {
      this.init();
    }
  }
};
</script>
