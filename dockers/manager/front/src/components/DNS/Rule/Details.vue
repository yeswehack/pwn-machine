<template>
  <div class=" row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">{{ value.name }}</div>
            <q-space />
            <div title="Rule type" class="text-mono">{{ value.type }}</div>
            <help-link
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section>
          <q-input v-model.number="form.ttl" type="number" label="TTL" />
          <component
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
          <log-list flat :domain="value.name" :type="value.type" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>
<script>
import EditTable from "src/components/EditTable.vue";
import HelpLink from "src/components/HelpLink.vue";
import LogList from "src/components/DNS/LogList.vue";
import RuleInput from "./RuleInput.vue";

import ResetAndSave from "src/components/ResetAndSave.vue";
import DeepForm from "src/mixins/DeepForm";
import db from "src/gql";

export default {
  mixins: [DeepForm],
  components: { EditTable, ResetAndSave, HelpLink, LogList },
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
  methods: {
    submit() {
      const patch = {
        ...this.form,
        records: this.form.records.map(r => ({ content: r.content, enabled: r.enabled }))
      };
      this.$apollo.mutate({
        mutation: db.dns.UPDATE_RULE,
        variables: { nodeId: this.value.nodeId, patch },
        refetchQueries: [{ query: db.dns.GET_RULES }]
      });
    }
  }
};
</script>

<style></style>
