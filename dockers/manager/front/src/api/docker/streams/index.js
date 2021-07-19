import * as fragments from "./fragments.js";
import * as mutations from "./mutations.js";
import * as queries from "./queries.js";
import * as subscriptions from "./subscriptions.js";

export default {
  ...fragments,
  ...subscriptions,
  ...mutations,
  ...queries
};
