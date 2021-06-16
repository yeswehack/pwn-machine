<template>
  <div class="q-gutter-md q-py-sm">
    <div class="row ">
      <div class="col q-mr-md">
        <q-card>
          <q-card-section>
            <div class="row items-center q-gutter-md">
              <div class="text-h6">{{ value.name }}</div>
              <q-space />
              <div title="Rule type" class="text-mono">
                {{ value.type }}
                <q-badge
                  v-if="value.isLua"
                  rounded
                  label="LUA"
                  class="q-ml-sm"
                />
              </div>
              <help-link
                href="https://doc.powerdns.com/authoritative/http-api/zone.html"
              />
            </div>
          </q-card-section>
          <q-card-section class="q-gutter-md">
            <q-input v-model.number="form.ttl" type="number" label="TTL" />
            <lua-editor v-if="value.isLua" v-model="form.records[0].content" />
            <component
              :is="formChildren.records"
              v-else
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
        <check-propagation :rule="value" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <log-card>
          <log-list
            short
            flat
            :domain="value.name.slice(0, -1)"
            :type="logType"
          />
        </log-card>
      </div>
    </div>
  </div>
</template>
<script>
import HelpLink from "src/components/HelpLink.vue";
import LogList from "src/components/DNS/Log/LogList.vue";
import RuleInput from "./RuleInput.vue";

import ResetAndSave from "src/components/ResetAndSave.vue";
import CheckPropagation from "./CheckPropagation.vue";
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import LuaEditor from "./LuaEditor.vue";
import LogCard from "src/components/LogCard.vue";

export default {
  components: {
    ResetAndSave,
    HelpLink,
    LogList,
    LuaEditor,
    LogCard,
    CheckPropagation
  },
  mixins: [DeepForm],
  formDefinition: {
    records: RuleInput,
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
      this.mutate({
        mutation: api.dns.rules.UPDATE_RULE,
        variables: { nodeId: this.value.nodeId, patch: this.form },
        refetchQueries: [{ query: api.dns.rules.LIST_RULES }],
        message: `${this.value.name} updated.`
      }).finally(done);
    }
  }
};
</script>
