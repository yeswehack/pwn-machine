<template>
  <q-form>
    <q-card style="min-width: 50vw" bordered>
      <q-card-section class="q-gutter-sm">
        <component
          :is="formChildren.containerName"
          v-model="form.containerName"
        />
        <q-input label="Command" v-model="form.cmd" />

        <q-list separator class="rounded-borders" bordered>
          <q-expansion-item label="Extra config" icon="star">
            <q-card>
              <q-card-section>
                <div class="column q-col-gutter-sm">
                  <div class="col">
                    <q-input
                      label="User"
                      v-model="form.user"
                      hint="format: <name|uid>[:<group|gid>]"
                    />
                  </div>
                  <div class="col">
                    <q-input label="Working directory" v-model="form.workDir" />
                  </div>
                  <div class="col">
                    <q-toggle label="Privileged" v-model="form.privileged" />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
          <component
            :is="formChildren.environment"
            v-model="form.environment"
          />
        </q-list>
      </q-card-section>
      <q-card-section>
        <pre>{{ form }}</pre>
      </q-card-section>
      <q-card-section>
        <reset-and-save :modified="modified" @save="submit" @reset="reset" />
      </q-card-section>
    </q-card>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ContainerSelect from "../Docker/Container/Form/ContainerSelect.vue";
import EnvironInputVue from "../Docker/Container/Form/EnvironInput.vue";
import ResetAndSave from "../ResetAndSave.vue";
import gql from "src/gql";
export default {
  mixins: [DeepForm],
  formDefinition: {
    user: null,
    workDir: null,
    privileged: false,
    cmd: "/bin/sh -c 'if which bash; then bash ; else sh ; fi'",
    containerName: ContainerSelect,
    environment: EnvironInputVue
  },
  components: { ContainerSelect, ResetAndSave },
  methods: {
    submit() {
      this.$apollo.mutate({
        mutation: gql.docker.SPAWN_SHELL,
        variables: { input: this.form }
      });
    }
  }
};
</script>

<style>
.no-top-border {
  border-top: none;
}
</style>
