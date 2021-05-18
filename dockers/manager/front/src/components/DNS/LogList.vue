<template>
  <q-table
    class="full-width"
    v-bind="$attrs"
    :columns="columns"
    dense
    @request="onRequest"
    :loading="$apollo.queries.dnsLogs.loading"
    :data="logs"
    :pagination.sync="pagination"
    no-data-label="No logs available."
    table-header-style="text-transform: capitalize"
  >
    <template #body-cell-date="{value}">
      <q-td auto-width>
        {{ value }}
      </q-td>
    </template>
    <template #body-cell-type="{value}">
      <q-td auto-width>
        {{ value }}
      </q-td>
    </template>
    <template #body-cell-error="{value}">
      <q-td auto-width>
        <q-badge color="negative" :label="value" v-if="value" />
      </q-td>
    </template>
    <template #body-cell-origin="{value}">
      <q-td auto-width>
        <a :href="`https://ip-api.com/${value}`" target="_blank">{{ value }}</a>
      </q-td>
    </template>
    <template #no-data="props">
      <q-btn
        round
        flat
        size="xs"
        icon="eva-loader-outline"
        :loading="$apollo.queries.dnsLogs.loading"
        class=" q-mr-md no-pointer-events"
      />
      {{ props.message }}
    </template>
  </q-table>
</template>

<script>
import api from "src/api";
import { date } from "quasar";

export default {
  props: {
    domain: { type: String, default: "*" },
    type: { type: String, default: "*" },
    hideTitle: { type: Boolean, default: false },
    rowsPerPage: { type: Number, default: 10 }
  },
  apollo: {
    dnsLogs: {
      query: api.dns.GET_LOGS,
      variables() {
        const { page, rowsPerPage } = this.pagination
        return {
          filter: { query: this.domain, type: this.type },
          cursor: { from: (page - 1) * rowsPerPage, size: rowsPerPage }
        };
      },
      fetchPolicy: "network-only",
      pollInterval: 5000
    }
  },
  methods: {
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination;
      this.pagination.page = page;
      this.pagination.rowsPerPage = rowsPerPage;
      this.$apollo.queries.dnsLogs.refetch();
    }
  },
  data() {
    const pagination = {
      rowsPerPage: this.rowsPerPage,
      rowsNumber: 1
    };
    const field = (name, opt = {}) => ({
      name,
      label: name,
      field: name,
      align: "left",
      ...opt
    });
    const columns = [
      field("date", {
        format: v => date.formatDate(v * 1000, "YYYY-MM-DD HH:mm:ss")
      }),
      field("origin"),
      field("type", { align: "center" }),
      field("query"),
      field("responses", {
        field: row => row.responses.map(r => r.rdata).join(", ")
      }),
      field("error")
    ];
    return {
      pagination,
      columns
    };
  },
  watch: {
    dnsLogs(dnsLogs) {
      this.pagination.rowsNumber = dnsLogs.total;
    }
  },
  computed: {
    rowNumber() {
      return this.logs?.total ?? 0;
    },
    logs() {
      return this.dnsLogs?.result ?? [];
    },
    from() {
      return 0;
    },
    size() {
      return this.pagination.rowsPerPage;
    },
    title() {
      if (this.hideTitle) return false;
      if (this.type == "*") {
        return `DNS logs for ${this.domain}`;
      }
      return `DNS logs for ${this.domain} of type ${this.type}`;
    }
  }
};
</script>

<style></style>
