<template>
  <div class="dns-log-table">
    <div class="row q-gutter-sm items-center">
      <div class="col">
        <q-input v-model="domain" filled label="Domain" />
      </div>
      <div class="col col-auto">
        <q-input v-model="type" filled label="Type" />
      </div>
    </div>
    <log-list
      bordered
      flat
      :rows-per-page="20"
      hide-title
      :domain="domain.slice(0, -1)"
      :type="type"
    />
  </div>
</template>

<script>
import LogList from "src/components/DNS/Log/LogList.vue";

export default {
  components: { LogList },
  data: () => ({ domain: "*", type: "*" })
};
</script>
<style lang="scss" scoped>
.dns-log-table {
  width: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  row-gap: 14px;
}
</style>
