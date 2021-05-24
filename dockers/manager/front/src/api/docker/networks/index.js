import * as fragments from "./fragments.js";
import * as mutations from "./mutations.js";
import * as queries from "./queries.js";

export default {
  ...fragments,
  ...mutations,
  ...queries
};
