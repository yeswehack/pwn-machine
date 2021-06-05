<template>
  <q-expansion-item label="Sticky Cookie" icon="fas fa-cookie-bite">
    <q-separator />
    <q-card>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.cookie.name" label="Name" />
        <div class="row">
          <q-select
            class="col"
            clearable
            v-model="form.cookie.sameSite"
            :options="sameSiteOptions"
            label="SameSite"
          />
          <q-toggle
            class="col col-auto"
            v-model="form.cookie.httpOnly"
            label="http-only"
          />
          <q-toggle
            class="col col-auto"
            v-model="form.cookie.secure"
            label="secure"
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
  data: () => ({ sameSiteOptions: ["none", "lax", "strict"] }),
  formDefinition: {
    cookie: {
      name: null,
      sameSite: null,
      httpOnly: null,
      secure: null
    }
  }
};
</script>
