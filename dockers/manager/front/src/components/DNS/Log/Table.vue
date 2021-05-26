<template>
  <div class="dns-log-table">
    <div class="row q-gutter-sm items-center">
      <div class="col">
        <q-input filled v-model="domain" label="Domain" />
      </div>
      <div class="col col-auto">
        <q-input filled v-model="type" label="Type" />
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
  data() {
    return { domain: "*", type: "*" };
  }
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
