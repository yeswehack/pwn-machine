<template>
  <div class="column full-width">
    <div class="row full-width">
      <q-table
        class="full-width"
        v-bind="$attrs"
        :columns="columns"
        dense
        :loading="$apollo.queries.logs.loading"
        :data="logs"
        hide-pagination
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
            <a :href="`https://ip-api.com/${value}`" target="_blank">{{
              value
            }}</a>
          </q-td>
        </template>
        <template #no-data="props">
          <q-btn
            round
            flat
            size="xs"
            icon="eva-loader-outline"
            :loading="$apollo.queries.logs.loading"
            class=" q-mr-md no-pointer-events"
          />
          {{ props.message }}
        </template>
      </q-table>
    </div>
    <div class="row q-gutter-md q-px-sm justify-end">
      <q-input
        v-model.number="pagination.rowsPerPage"
        dense
        type="number"
        class="col col-auto"
        label="Row per page"
        style="max-width: 7em"
      />
      <q-input
        v-model.number="page"
        dense
        max="1000"
        min="1"
        type="number"
        class="col col-auto"
        label="Page"
        style="max-width: 7em"
      />
      <q-pagination
        class="col col-auto"
        v-model="page"
        :max="page + 5"
        :max-pages="4"
        :boundary-numbers="false"
        direction-links
      />
    </div>
  </div>
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
    logs: {
      query: api.dns.GET_LOGS,
      variables() {
        return {
          filter: { query: this.domain, type: this.type },
          cursor: {
            from: this.from,
            size: this.size
          }
        };
      },
      fetchPolicy: "network-only",
      pollInterval: 5000,
      update: data => data.dnsLogs.result
      /*
      subscribeToMore: {
        document: gql`
          subscription getLog($filter: DnsLogFilter) {
            dnsLogs(filter: $filter) {
              origin
              time
              domain
              type
            }
          }
        `,
        skip() {
          return this.page > 1;
        },
        variables() {
          return {
            filter: { domain: this.domain, type: this.type }
          };
        },
        updateQuery(previousResult, { subscriptionData }) {
          if (this.page > 1) return;
          if (subscriptionData.data.dnsLogs) {
            return {
              dnsLogs: [
                subscriptionData.data.dnsLogs,
                ...previousResult.dnsLogs
              ]
            };
          }
        }
      }*/
    }
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
      columns,
      page: 1
    };
  },
  watch: {
    page(v) {
      this.page = Math.min(Math.max(v, 1), 500);
      if (this.page > 1) {
        this.$apollo.subscriptions.logs.stop();
      } else {
        this.$apollo.subscriptions.logs.start();
      }
    }
  },
  computed: {
    from() {
      return Math.max(this.page - 1, 0) * this.size;
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
