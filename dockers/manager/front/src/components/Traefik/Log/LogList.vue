<template>
  <q-table
    v-bind="$attrs"
    ref="table"
    class="full-width scroll thin-scrollbar"
    :columns="columns"
    dense
    :loading="$apollo.loading"
    :data="logs"
    :pagination.sync="pagination"
    no-data-label="No logs available."
    table-header-style="text-transform: capitalize"
    @request="onRequest"
  >
    <template #body-cell="props">
      <q-td auto-width :props="props">
        {{ props.value }}
      </q-td>
    </template>
    <template #body-cell-path="{value}">
      <q-td style="max-width: 300px" class="ellipsis">
        {{ value }}
        <q-popup-edit :value="value">
          <q-input :value="value" readonly dense autofocus />
        </q-popup-edit>
      </q-td>
    </template>
    <template #body-cell-host="{value}">
      <q-td>
        {{ value }}
      </q-td>
    </template>
    <template #body-cell-origin="{value}">
      <q-td auto-width>
        <a :href="`https://ip-api.com/${value}`" target="_blank">{{ value }}</a>
      </q-td>
    </template>
    <template #body-cell-routerName="{value}">
      <q-td auto-width>
        <router-link v-if="value" :name="value" />
      </q-td>
    </template>
    <template #body-cell-serviceName="{value}">
      <q-td auto-width>
        <service-link v-if="value" :name="value" />
      </q-td>
    </template>
    <template #body-cell-entrypointName="{value}">
      <q-td auto-width align="center">
        <entrypoint-link v-if="value" :name="value" />
      </q-td>
    </template>
    <template #body-cell-status="{value}">
      <q-td auto-width>
        <div :class="statusColor(value)">{{ value }}</div>
      </q-td>
    </template>

    <template #no-data="props">
      <q-btn
        round
        flat
        size="xs"
        icon="eva-loader-outline"
        :loading="$apollo.loading"
        class="q-mr-md no-pointer-events"
      />
      {{ props.message }}
    </template>
  </q-table>
</template>

<script>
import api from "src/api";
import { date } from "quasar";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import ServiceLink from "src/components/Traefik/Service/Link.vue";
import EntrypointLink from "src/components/Traefik/Entrypoint/Link.vue";

export default {
  components: { RouterLink, ServiceLink, EntrypointLink },
  props: {
    short: { type: Boolean, default: false },
    entrypoint: { type: Array, default: () => [] },
    router: { type: Array, default: () => [] },
    service: { type: Array, default: () => [] },
    rowsPerPage: { type: Number, default: 10 }
  },
  apollo: {
    traefikLogs: {
      query: api.traefik.logs.LIST_LOGS,
      variables() {
        const { page, rowsPerPage } = this.pagination;
        return {
          filter: {
            routers: this.router,
            entrypoints: this.entrypoint,
            services: this.service
          },
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
    let columns = [];
    if (this.short) {
      columns = [
        field("date", {
          format: v => date.formatDate(v, "YYYY-MM-DD HH:mm:ss")
        }),
        field("origin"),
        field("method", { align: "center" }),
        field("host", { field: r => `${r.host}:${r.port}` }),
        field("path"),
        field("status")
      ];
    } else {
      columns = [
        field("date", {
          format: v => date.formatDate(v, "YYYY-MM-DD HH:mm:ss")
        }),
        field("entrypointName", { label: "Entrypoint" }),
        field("origin"),
        field("method"),
        field("host", { field: r => `${r.host}:${r.port}` }),
        field("path"),
        field("protocol"),
        field("status"),
        field("routerName", { label: "Router" }),
        field("serviceName", { label: "Service" })
      ];
    }
    return { pagination, columns };
  },
  computed: {
    rowNumber() {
      return this.logs?.total ?? 0;
    },
    logs() {
      return this.traefikLogs?.result ?? [];
    },
    from() {
      return 0;
    },
    size() {
      return this.pagination.rowsPerPage;
    }
  },
  watch: {
    traefikLogs(traefikLogs) {
      this.pagination.rowsNumber = traefikLogs.total;
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
    statusColor(status) {
      if (status >= 200 && status < 300) {
        return "text-green";
      }
      if (status >= 300 && status < 400) {
        return "text-yellow";
      }
      if (status >= 400 && status < 600) {
        return "text-red";
      }
      return "";
    },
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination;
      this.pagination.page = page;
      this.pagination.rowsPerPage = rowsPerPage;
      this.$apollo.queries.traefikLogs.refetch();
    }
  }
};
</script>
