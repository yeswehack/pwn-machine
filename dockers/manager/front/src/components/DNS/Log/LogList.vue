<template>
  <q-table
    v-bind="$attrs"
    ref="table"
    class="full-width scroll thin-scrollbar"
    :columns="columns"
    dense
    :loading="$apollo.queries.dnsLogs.loading"
    :data="logs"
    :pagination.sync="pagination"
    no-data-label="No logs available."
    table-header-style="text-transform: capitalize"
    @request="onRequest"
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
        class="q-mr-md no-pointer-events"
      />
      {{ props.message }}
    </template>
  </q-table>
</template>

<script>
import api from "src/api";
import { date } from "quasar";
import _ from "lodash";

export default {
  props: {
    domain: { type: String, default: "*" },
    type: { type: String, default: "*" },
    rowsPerPage: { type: Number, default: 10 },
    short: { type: Boolean, default: false }
  },
  apollo: {
    dnsLogs: {
      query: api.dns.GET_LOGS,
      variables() {
        const { page, rowsPerPage } = this.pagination;
        return {
          filter: { query: this.domain, type: this.type },
          cursor: { from: (page - 1) * rowsPerPage, size: rowsPerPage }
        };
      },
      fetchPolicy: "network-only",
      pollInterval: 5000
    }
  },
  data() {
    const pagination = {
      page: 1,
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
      field("date"),
      field("origin"),
      field("type", { align: "center" }),
      field("query")
    ];
    return { pagination, columns };
  },
  computed: {
    rowNumber() {
      return this.logs?.total ?? 0;
    },
    logs() {
      return _.orderBy(this.dnsLogs?.result ?? [], "date", "desc");
    },
    from() {
      return 0;
    },
    size() {
      return this.pagination.rowsPerPage;
    }
  },
  watch: {
    dnsLogs(dnsLogs) {
      this.pagination.rowsNumber = dnsLogs.total;
    }
  },
  mounted() {
    const rowHeight = 28.5;
    const table = this.$refs.table.$el;
    const inner = table.querySelector(".q-table__middle");
    const height = inner.getBoundingClientRect().height;
    this.pagination.rowsPerPage = Math.floor(height / rowHeight - 1);
  },
  methods: {
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination;
      this.pagination.page = page;
      this.pagination.rowsPerPage = rowsPerPage;
      this.$apollo.queries.dnsLogs.refetch();
    }
  }
};
</script>
