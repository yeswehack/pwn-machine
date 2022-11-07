<template>
  <tab-page>
    <q-route-tab
      label="Password"
      icon="eva-lock"
      :to="{ name: 'configPassword' }"
    />
    <q-route-tab
      v-if="0"
      label="2-factor auth"
      icon="eva-keypad"
      :to="{ name: 'config2fa' }"
    />
  </tab-page>
</template>

<script>
import TabPage from "components/TabPage.vue";

export default {
  components: { TabPage },
};
</script>
