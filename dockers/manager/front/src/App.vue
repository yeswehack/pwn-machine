<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
import { Dark } from "quasar";
import Vue from "vue"


function getMutationName(m){
  const def = m.definitions.find(d=>d.kind == "OperationDefinition")
  const name = def.name.value
  return name
}

Vue.mixin({
  methods: {
    async runMutation(mutation, variables, message = null, update=null) {
      console.log(mutation)
      const mutationName = getMutationName(mutation)
      
      try {
        await this.$apollo.mutate({
          mutation,
          variables,
          update: (store, {data}) => {
            if (update === null) return
            return update(store, data[mutationName]) 
          }
        })
        if (message) {
          this.$q.notify({
            color: "positive",
            message
          })
        }
        return true
      } catch (e) {
        this.$q.notify({
          color: "negative",
          message: e.message
        })
        return false
      }
    }
  }
})

Dark.set(true);
export default {
  name: "App",
};
</script>
<style lang="scss">
* {
  box-sizing: border-box;
}
</style>
