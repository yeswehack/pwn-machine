<template>
  <q-card bordered style="width: 700px; max-width: 80vw;">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new DNS zone</div>
          <q-space />
          <a
            class="text-white"
            href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            target="_blank"
          >
            <q-icon size="sm" name="help" />
          </a>
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <div>
          <q-input
            filled
            v-model="formData.name"
            label="name"
            hint="example.com"
          />
        </div>
        <div>
          <q-input
            filled
            v-model="formData.nameserver"
            label="nameserver"
            hint="ns.example.com"
          />
        </div>
        <div>
          <q-input
            filled
            v-model="formData.postmaster"
            label="postmaster"
            hint="postmaster@example.com"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            v-model="formData.serial"
            label="serial"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            v-model="formData.refresh"
            label="refresh"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            v-model="formData.retry"
            label="retry"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            v-model="formData.expire"
            label="expire"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            v-model="formData.ttl"
            label="ttl"
          />
        </div>
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md q-gutter-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: {},
  methods: {
    submit() {
      this.$emit("submit", this.formData);
    }
  }
};
</script>
