
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Source criterion">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <component :is="formChildren.ipStrategy" label="Ip strategy" v-model="form.ipStrategy" />
      <q-input label="Request header name" v-model="form.requestHeaderName" />
      <q-toggle label="Request host" v-model="form.requestHost" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ipStrategy from './ipStrategy.vue';
export default {
    components: {  ipStrategy },
    mixins: [DeepForm],
    formDefinition: {
  ipStrategy: ipStrategy,
  requestHeaderName: null,
  requestHost: null,
},
}
</script>
