<template>
  <BaseTable
    ref="table"
    name="rule"
    :loading="$apollo.loading"
    :data="rules"
    :columns="columns"
    @deleteRow="deleteRule"
  >
    <template #body-cell-zone="{value}">
      <div class="q-gutter-sm row">
        <ZoneLink :name="value" />
      </div>
    </template>
    <template #body-cell-enabled="{value, row}">
      <q-toggle
        :value="value"
        :color="value ? 'positive' : 'negative'"
        keep-color
        @input="v => toggleRule(row, v)"
      /> </template
    ><!-- 
    <template v-slot:details="{ row }">
      <RuleDetails :rule="row" />
    </template>
    <template v-slot:popup="{ row, closePopup }">
      <CreateRule :value="row" @close="closePopup" :edit="false" />
    </template> -->
  </BaseTable>
</template>

<script>
import db from "src/gql";
import BaseTable from "../../components/BaseTable2.vue";
//import RuleDetails from "src/components/DNS/Rule/Details.vue";
import ZoneLink from "src/components/DNS/Zone/Link.vue";
//import CreateRule from "src/components/DNS/Rule/Create.vue";

export default {
  components: { BaseTable, ZoneLink },
  apollo: {
    rules: {
      query: db.dns.GET_RULES,
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
      ...opt
    });

    const columns = [
      field("zone"),
      field("name"),
      field("type"),
      field("ttl", { label: "TTL" }),
      field("records", {
        format: r => r.map(r => r.content).join(", ")
      }),
      field("enabled", { field: r => this.isEnabled(r) })
    ];
    return { columns };
  },
  methods: {
    deleteRule(rule) {
      const variables = {
        zone: rule.zone,
        name: rule.name,
        type: rule.type
      };
      this.runMutation(
        deleteDnsRule,
        variables,
        `Rule ${rule.type} ${rule.name} deleted.`,
        store => {
          const data = store.readQuery({ query: getRules });
          data.dns.rules = data.dns.rules.filter(r => r.id != rule["id"]);
          store.writeQuery({ query: getRules, data });
        }
      );
    },

    toggleRule(r, enable) {
      const mutation = enable ? enableDnsRule : disableDnsRule;
      const variables = {
        zone: r.zone,
        name: r.name,
        type: r.type
      };
      this.runMutation(
        mutation,
        variables,
        `Rule ${r.type} ${r.name} ${enable ? "enabled" : "disabled"}.`
      );
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
