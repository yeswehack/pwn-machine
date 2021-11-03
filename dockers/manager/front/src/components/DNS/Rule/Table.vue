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
      <q-badge v-if="row.isLua" rounded label="LUA" class="q-ml-sm" />
    </template>
    <template #body-cell-records="{row, value}">
      <pre v-if="row.isLua">{{ value }}</pre>
      <span v-else>{{ value }}</span>
    </template>
    <template #body-cell-enabled="{row, value}">
      <q-toggle
        :value="value"
        :color="value ? 'positive' : 'negative'"
        keep-color
        @input="v => toggleRule(row, v)"
      />
    </template>
    <template #details="{row}">
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
  created() {
    this.$root.$on("refresh", () => this.$apollo.queries.rules.refetch());
  },
  methods: {
    createRule() {
      this.$q.dialog({
        component: ZoneDialog,
        parent: this
      });
    },
    toggleRule(rule, value) {
      this.mutate({
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
          this.mutate({
            mutation: api.dns.rules.DELETE_RULE,
            variables: { nodeId: rule.nodeId },
            refetchQueries: [{ query: api.dns.rules.LIST_RULES }],
            message: `(${rule.type}) ${rule.name} deleted`
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
