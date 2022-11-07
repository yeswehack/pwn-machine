<template>
    <q-table
      title="DNS Propagation"
      :columns="columns"
      :data="data"
      :loading="$apollo.queries.dnsRuleCheckPropagation.loading"
      :rows-per-page-options="[0]"
      hide-pagination
    >
      <template #body-cell-records="props">
        <q-td :props="props">
          <div
            class="row justify-end q-gutter-sm"
            :class="{ error: !isMatching(props.value) }"
          >
            <div v-for="(r, idx) of props.value" :key="idx">{{ r }}</div>
          </div>
        </q-td>
      </template>
      <template v-if="rule.isLua" #no-data>Propagation check is not supported for LUA records</template>
      <template #bottom></template>
    </q-table>
</template>

<script>
import api from "src/api";
export default {
  props: {
    rule: { type: Object, required: true }
  },
  apollo: {
    dnsRuleCheckPropagation: {
      query: api.dns.rules.CHECK_PROPAGATION,
      variables() {
        return { nodeId: this.rule.nodeId };
      },
      skip() {
        return this.rule.isLua;
      }
    }
  },
  data() {
    const col = (name, props = {}) => ({
      name,
      label: name,
      sortable: true,
      field: name,
      ...props
    });
    const columns = [
      col("name", { label: "Resolver", align: "left" }),
      col("records", { label: "Result" })
    ];
    return { columns };
  },
  computed: {
    data() {
      return this.dnsRuleCheckPropagation ?? [];
    },
    expected() {
      const local = (this.dnsRuleCheckPropagation ?? []).find(
        r => r.name === "Local"
      );
      return local?.records ?? [];
    }
  },
  methods: {
    isMatching(records) {
      return records.join("") === this.expected.join("");
    },
    check() {
      this.$apollo.query({
        query: api.dns.rules.CHECK_PROPAGATION
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.error {
  color: $negative;
}
</style>
