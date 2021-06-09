<template>
  <q-expansion-item label="Sticky Cookie" icon="fas fa-cookie-bite">
    <q-separator />
    <q-card>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.cookie.name" label="Name" />
        <div class="row">
          <q-select
            v-model="form.cookie.sameSite"
            label="SameSite"
            class="col"
            :options="sameSiteOptions"
            clearable
          />
          <q-toggle
            v-model="form.cookie.httpOnly"
            label="http-only"
            class="col col-auto"
          />
          <q-toggle
            v-model="form.cookie.secure"
            label="secure"
            class="col col-auto"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  formDefinition: {
    cookie: {
      name: null,
      sameSite: null,
      httpOnly: null,
      secure: null
    }
  },
  data: () => ({ sameSiteOptions: ["none", "lax", "strict"] })
};
</script>
