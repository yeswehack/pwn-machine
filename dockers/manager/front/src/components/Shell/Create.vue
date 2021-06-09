<template>
  <div>
    <q-card-section>
      <div class="column q-gutter-sm">
        <component
          :is="formChildren.containerName"
          ref="containerName"
          v-model="form.containerName"
        />
        <q-input v-model="form.cmd" label="Command" />

        <q-list separator class="rounded-borders" bordered>
          <q-expansion-item label="Extra config" icon="star">
            <q-card>
              <q-card-section>
                <div class="column q-col-gutter-sm">
                  <div class="col">
                    <q-input
                      v-model="form.user"
                      label="User"
                      hint="format: <name|uid>[:<group|gid>]"
                    />
                  </div>
                  <div class="col">
                    <q-input v-model="form.workdir" label="Working directory" />
                  </div>
                  <div class="col">
                    <q-toggle v-model="form.privileged" label="Privileged" />
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
      </div>
    </q-card-section>
    <q-card-section>
      <reset-and-save
        :modified="modified"
        :validate="validate"
        @save="submit"
        @reset="reset"
      />
    </q-card-section>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ContainerSelect from "../Docker/Container/Form/ContainerSelect.vue";
import EnvironInputVue from "../Docker/Container/Form/EnvironInput.vue";
import ResetAndSave from "../ResetAndSave.vue";
import api from "src/api";

export default {
  components: { ContainerSelect, ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    user: null,
    workdir: null,
    privileged: false,
    cmd: "/bin/sh -c 'if which bash; then bash ; else sh ; fi'",
    containerName: ContainerSelect,
    environment: EnvironInputVue
  },
  methods: {
    submit() {
      this.mutate({
        mutation: api.docker.shells.SPAWN_SHELL,
        variables: { input: this.form },
        refetchQueries: [{ query: api.docker.shells.LIST_SHELLS }]
      }).then(result => {
        const id = result.nodeId;
        this.$router.push({ name: "shellId", params: { id } });
      });
    },
    validate() {
      return this.$refs.containerName.validate();
    }
  }
};
</script>

<style>
.no-top-border {
  border-top: none;
}
</style>
