<template>
  <q-form class="flex flex-center" @submit="submit">
    <q-card bordered style="width:500px">
      <q-card-section class="text-h6">
        Change password
      </q-card-section>
      <q-separator />
      <q-card-section>
        <q-input label="New password" type="password" v-model="password" />
        <q-input label="Confirm password" type="password" v-model="repeated" />
      </q-card-section>
      <q-card-actions vertical>
        <q-btn color="positive" :disable="password !== repeated" type="submit">
          Submit
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-form>
</template>

<script>
import api from "src/api";

export default {
  data: () => ({
    password: "",
    repeated: ""
  }),
  methods: {
    async submit() {
      if (this.password !== this.repeated) return;
      await this.$apollo.mutate({
        mutation: api.auth.UPDATE_PASSWORD,
        variables: { password: this.password }
      });
    }
  }
};
</script>
