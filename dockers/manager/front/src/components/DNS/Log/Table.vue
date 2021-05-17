<template>
  <div class="column full-width q-col-gutter-md">
    <div class="row q-gutter-md ">
      <div class="col">
        <q-input filled v-model="domain" label="Domain" />
      </div>
      <div class="col col-auto">
        <q-input filled v-model="type" label="Type" />
      </div>
      <div class="col col-auto q-pt-sm">
        <q-btn
          icon="eva-cloud-download-outline"
          title="Download all matching log as json"
          round
          size="md"
          color="primary"
        />
      </div>
      <div class="col col-auto q-pt-sm">
        <q-btn
          icon="eva-trash"
          title="Delete all matching log"
          round
          size="md"
          color="negative"
        />
      </div>
    </div>
    <log-list
      bordered
      flat
      :rows-per-page="20"
      hide-title
      :domain="domain"
      :type="type"
    />
  </div>
</template>

<script>
import LogList from "src/components/DNS/LogList.vue";
export default {
  components: { LogList },
  data() {
    return { domain: "*", type: "*" };
  }
};
</script>

<style></style>
