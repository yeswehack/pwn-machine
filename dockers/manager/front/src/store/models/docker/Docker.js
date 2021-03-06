
import { Model } from '@vuex-orm/core'
import Image from "./Image.js"


export default class Docker extends Model {
  // This is the name used as module name of the Vuex Store.
  static entity = 'docker'

  // List of all fields (schema) of the post model. `this.attr` is used
  // for the generic field type. The argument is the default value.
  static fields () {
    return {
      images: Image,
    }
  }
}