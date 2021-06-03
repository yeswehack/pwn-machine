// import something here

import { notify } from "src/utils";

// "async" is optional;
// more info on params: https://quasar.dev/quasar-cli/boot-files
export default ({ Vue }) => {
  Vue.mixin({
    methods: {
      mutate: function({ message, ...opt }) {
        return new Promise((resolve, reject) => {
          console.log(opt)
          return this.$apollo.mutate(opt).then(notify(message)).then(r => {
            if (r.success){
              resolve(r.result)
            } else {
              reject(r.error)
            }
          });
        });
      }
    }
  });
};
