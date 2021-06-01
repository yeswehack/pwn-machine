<template>
  <base-table
    ref="table"
    name="rule"
    :query="$apollo.queries.rules"
    :data="rules"
    :columns="columns"
    @create="createRule"
    @clone="cloneRule"
    @delete="deleteRule"
  >
    <template #body-cell-zone="{value}">
      <div class="q-gutter-sm row">
        <zone-link :name="value" />
      </div>
    </template>
    <template #body-cell-type="{row, value}">
      {{ value }}
      <q-badge rounded label="LUA" class="q-ml-sm" v-if="row.isLua" />
    </template>
    <template #body-cell-enabled="{row, value}">
      <q-toggle
        :value="value"
        :color="value ? 'positive' : 'negative'"
        keep-color
        @input="v => toggleRule(row, v)"
      />
    </template>
    <template v-slot:details="{ row }">
      <rule-details :value="row" />
    </template>
  </base-table>
</template>

<script>
import api from "src/api";
import BaseTable from "src/components/BaseTable.vue";
import RuleDetails from "src/components/DNS/Rule/Details.vue";
import ZoneLink from "src/components/DNS/Zone/Link.vue";
import ZoneDialog from "src/components/DNS/Rule/Dialog.vue";

export default {
  components: { BaseTable, ZoneLink, RuleDetails },
  apollo: {
    rules: {
      query: api.dns.rules.LIST_RULES,
      update: data => data.dnsRules
    }
  },
  created() {
    this.$root.$on("refresh", () => this.$apollo.queries.rules.refetch());
  },
  data() {
    const field = (name, opt = {}) => ({
      name: name,
      align: "left",
      label: name,
      field: name,
      sortable: true,
      autoWidth: true,
      ...opt
    });

    const columns = [
      field("zone"),
      field("name"),
      field("type"),
      field("ttl", { label: "TTL" }),
      field("records", {
        format: r => r.map(r => r.content).join(", "),
        autoWidth: false
      }),
      field("enabled", { field: r => this.isEnabled(r) })
    ];
    return { columns };
  },
  methods: {
    createRule() {
      this.$q.dialog({
        component: ZoneDialog,
        parent: this
      });
    },
    toggleRule(rule, value) {
      this.$apollo.mutate({
        mutation: api.dns.rules.ENABLE_RULE,
        variables: { nodeId: rule.nodeId, enabled: value },
        refetchQueries: [{ query: api.dns.rules.LIST_RULES }]
      });
    },
    cloneRule(rule) {
      this.$q.dialog({
        component: ZoneDialog,
        parent: this,
        rule
      });
    },
    deleteRule(rule) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete (${rule.type}) ${rule.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.$apollo.mutate({
            mutation: api.dns.rules.DELETE_RULE,
            variables: { nodeId: rule.nodeId },
            refetchQueries: [{ query: api.dns.rules.LIST_RULES }]
          });
        });
    },
    isEnabled(r) {
      const enabled = r["records"].reduce((p, c) => ~~c["enabled"] + p, 0);
      if (enabled === r["records"].length) {
        return true;
      }
      return enabled === 0 ? false : "partial";
    }
  }
};
</script>
