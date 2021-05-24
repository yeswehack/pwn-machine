<template>
  <div class="full-width column q-gutter-md">
    <div class="col col-auto full-width">
      <div class="row q-gutter-sm items-center">
        <div class="col">
          <q-input filled v-model="domain" label="Domain" />
        </div>
        <div class="col col-auto">
          <q-input filled v-model="type" label="Type" />
        </div>
        <div class="col col-auto">
          <q-btn
            icon="eva-cloud-download-outline"
            title="Download all matching log as json"
            round
            size="md"
            color="primary"
          />
        </div>
        <div class="col col-auto">
          <q-btn
            icon="eva-trash"
            title="Delete all matching log"
            round
            size="md"
            color="negative"
          />
        </div>
      </div>
    </div>
    <div class="col full-width">
      <log-list
        bordered
        flat
        :rows-per-page="20"
        hide-title
        :domain="domain.slice(0, -1)"
        :type="type"
      />
    </div>
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
