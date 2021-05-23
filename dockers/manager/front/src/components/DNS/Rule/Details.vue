<template>
  <div class=" row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">{{ value.name }}</div>
            <q-space />
            <div title="Rule type" class="text-mono">
              {{ value.type }}
              <q-badge rounded label="LUA" class="q-ml-sm" v-if="value.isLua" />
            </div>
            <help-link
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-gutter-md">
          <q-input v-model.number="form.ttl" type="number" label="TTL" />
          <lua-editor v-model="form.records[0].content" v-if="value.isLua" />
          <component
            v-else
            :is="formChildren.records"
            v-model="form.records"
            object-key="content"
            label="Records"
          />
        </q-card-section>
        <q-card-section>
          <reset-and-save
            size="sm"
            padding="sm"
            :modified="modified"
            @reset="reset"
            @save="submit"
          />
        </q-card-section>
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="text-h6">Logs</div>
        </q-card-section>
        <q-card-section>
          <log-list flat :domain="value.name.slice(0, -1)" :type="logType" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>
<script>
import HelpLink from "src/components/HelpLink.vue";
import LogList from "src/components/DNS/LogList.vue";
import RecordInput from "./RecordInput.vue";

import ResetAndSave from "src/components/ResetAndSave.vue";
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import LuaEditor from "./LuaEditor.vue";

export default {
  mixins: [DeepForm],
  components: { ResetAndSave, HelpLink, LogList, LuaEditor },
  formDefinition: {
    records: RecordInput,
    ttl: 3600
  },
  data() {
    const recordColumns = [
      {
        name: "content",
        align: "left",
        label: "content",
        field: "content",
        headerStyle: "width: 90%"
      },
      {
        name: "enabled",
        align: "left",
        label: "enabled",
        field: "enabled",
        headerStyle: "width: 10%"
      }
    ];
    return { ttl: 0, recordColumns, records: [] };
  },
  computed: {
    logType() {
      return this.value.type;
    }
  },
  methods: {
    submit(done) {
      const patch = {
        ...this.form,
        records: this.form.records.map(r => ({
          content: r.content,
          enabled: r.enabled
        }))
      };
      this.$apollo
        .mutate({
          mutation: api.dns.rules.UPDATE_RULE,
          variables: { nodeId: this.value.nodeId, patch },
          refetchQueries: [{ query: api.dns.rules.LIST_RULES }]
        })
        .then(done);
    }
  }
};
</script>

<style></style>
