<template>
  <q-list dark >
    <slot name="before"></slot>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.nameserver"
            label="Nameserver"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.postmaster"
            label="Postmaster"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.refresh"
            type="number"
            label="Refresh"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.retry"
            type="number"
            label="Retry"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.expire"
            type="number"
            label="Expire"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label>
          <q-input
            v-bind="$attrs"
            v-model="formData.ttl"
            type="number"
            label="TTL"
          />
        </q-item-label>
      </q-item-section>
    </q-item>
    <slot name="after"></slot>
    <q-item v-if="!noButtons">
      <q-item-section>
        <ResetAndSave :modified="modified" @reset="reset" @save="submit" />
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script>
import ResetAndSave from "src/components/ResetAndSave.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  props: {
    noButtons: { type: Boolean, default: false }
  },
  components: { ResetAndSave }
};
</script>

<style></style>
