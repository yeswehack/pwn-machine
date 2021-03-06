<template>
  <BaseTable
    ref="table"
    name="rule"
    :rkey="r => r.zone + r.name + r.type + r.record"
    :loading="loading"
    :data="rules"
    :columns="columns"
    @cloneRow="cloneRule"
  >
    <template #body-cell-zone="{row}">
      <div class="q-gutter-sm row">
        <ZoneLink :name="row.zone.slice(0, -1)" />
      </div>
    </template>
    <template #body-cell-enabled="{row}">
      <q-toggle
        :value="isEnabled(row)"
        color="green"
        @input="v => toggleRule(row, v)"
      />
    </template>
    <template #popup>
      <CreateRecord />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "../../components/BaseTable.vue";
import ZoneLink from "src/components/DNS/Zone/Link.vue";
import CreateRecord from "src/components/DNS/Record/Create.vue";
import gql from "graphql-tag";

const ruleFragment = gql`
  fragment ruleFragment on Rule {
    id
    name
    records {
      content
      enabled
    }
    type
    zone
    ttl
  }
`;

const enableDnsRule = gql`
  mutation enableDnsRule($zone: String!, $name: String!, $type: String!) {
    enableDnsRule(zone: $zone, name: $name, type: $type) {
      rule {
        ...ruleFragment
      }
    }
  }
  ${ruleFragment}
`;

const disableDnsRule = gql`
  mutation disableDnsRule($zone: String!, $name: String!, $type: String!) {
    disableDnsRule(zone: $zone, name: $name, type: $type) {
      rule {
        ...ruleFragment
      }
    }
  }
  ${ruleFragment}
`;

const getRules = {
  query: gql`
    query getRules {
      dns {
        rules {
          ...ruleFragment
        }
      }
    }
    ${ruleFragment}
  `,
  update: data => data.dns.rules
};

export default {
  components: { BaseTable, ZoneLink, CreateRecord },
  methods: {
    createRecord() {},
    update(data) {
      return data.dns.records;
    },
    cloneRule({id}){
      console.log(id)
    },
    toggleRule(r, enable) {
      if (enable) {
        this.$apollo.mutate({
          mutation: enableDnsRule,
          variables: {
            zone: r["zone"],
            name: r["name"],
            type: r["type"]
          }
        });
      } else {
        this.$apollo.mutate({
          mutation: disableDnsRule,
          variables: {
            zone: r["zone"],
            name: r["name"],
            type: r["type"]
          }
        });
      }
      return r;
    },
    isEnabled(r) {
      const enabled = r["records"].reduce((p, c) => ~~c["enabled"] + p, 0);
      return enabled === r["records"].length
        ? true
        : enabled === 0
        ? false
        : "partial";
    }
  },
  apollo: {
    rules: getRules
  },
  computed: {
    loading() {
      return this.$apollo.queries.rules.loading;
    }
  },
  data() {
    const columns = [
      {
        name: "zone",
        align: "left",
        label: "Zone",
        field: "zone",
        format: val => `${val}`,
        sortable: true
      },
      {
        name: "name",
        label: "Name",
        align: "left",
        field: "name",
        format: n => n.slice(0, -1),
        sortable: true
      },
      {
        name: "type",
        label: "Type",
        align: "left",
        field: "type",
        sortable: true
      },
      {
        name: "ttl",
        label: "TTL",
        align: "left",
        field: "ttl",
        sortable: true
      },
      {
        name: "records",
        label: "Records",
        align: "left",
        field: row => row.records.map(r => r.content).join(", "),
        sortable: true
      },
      {
        name: "enabled",
        label: "Enabled",
        align: "left",
        field: r => isEnabled(r),
        sortable: true
      }
    ];
    return {
      columns
    };
  }
};
</script>

<style></style>
