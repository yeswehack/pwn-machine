
import { Model } from '@vuex-orm/core'

export default class Image extends Model {
  // This is the name used as module name of the Vuex Store.
  static entity = 'dockerImages'

  // List of all fields (schema) of the post model. `this.attr` is used
  // for the generic field type. The argument is the default value.
  static fields () {
    return {
      id: this.attr(null),
      name: this.attr('')
    }
  }
}