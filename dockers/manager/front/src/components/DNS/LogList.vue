<template>
  <q-table
    v-bind="$attrs"
    :columns="columns"
    dense
    :loading="$apollo.loading"
    :data="logs"
    :pagination="pagination"
    no-data-label="No logs available."
    table-header-style="text-transform: capitalize"
  >
    <template #top>
      <div class="text-h6 q-py-md" v-if="!hideTitle">
        {{ title }}
      </div>
    </template>
    <template #body-cell-origin="{value}">
      <q-td>
        <a :href="`https://ip-api.com/${value}`" target="_blank">{{ value }}</a>
      </q-td>
    </template>
    <template #body-cell-remove>
      <q-td auto-width>
        <div class="row justify-center">
          <q-btn icon="eva-trash" round size="sm" color="negative" />
        </div>
      </q-td>
    </template>
    <template #no-data="props">
      <q-btn
        round
        flat
        size="xs"
        icon="eva-loader-outline"
        :loading="$apollo.loading"
        class=" q-mr-md no-pointer-events"
      />
      {{ props.message }}
    </template>
  </q-table>
</template>

<script>
//import graphql from "src/gql/dns";
const {
  queries: { getDnsLogs }
} = {};

export default {
  props: {
    domain: { type: String, default: "*" },
    type: { type: String, default: "*" },
    hideTitle: { type: Boolean, default: false },
    rowsPerPage: { type: Number, default: 10 }
  },
  created() {
    this.$root.$on("refresh", () => this.$apollo.queries.logs.refetch());
  },
  data() {
    const pagination = {
      rowsPerPage: this.rowsPerPage
    };
    const field = (name, opt = {}) => ({
      name,
      label: name,
      field: name,
      align: "left",
      sortable: true,
      ...opt
    });
    const columns = [
      field("origin"),
      field("domain"),
      field("type"),
      field("time"),
      field("remove", { align: "center", sortable: false })
    ];
    return {
      pagination,
      columns
    };
  },
  computed: {
    title() {
      if (this.hideTitle) return false;
      if (this.type == "*") {
        return `DNS logs for ${this.domain}`;
      }
      return `DNS logs for ${this.domain} of type ${this.type}`;
    }
  },
  apollo: {
    logs: {
      query: getDnsLogs,
      variables() {
        return {
          domain: this.domain,
          type: this.type
        };
      },
      throttle: 200,
      debounce: 200,
      update: data => data.dns.logs
    }
  }
};
</script>

<style></style>
