import { exportFile } from "quasar";

export function showErrors(vm, errors) {
  if (errors) {
    for (const error of errors) {
      vm.$q.notify({
        type: "negative",
        position: "top",
        message: error.msg
      });
    }
  }
}

export function shortName(name) {
  if (name.match(/^[a-f0-9]{64}$/)) {
    return name.substr(0, 12);
  }
  if (name.endsWith(":latest")) {
    return name.substr(name, name.length - 7)
  }

  return name;
}

export function shortDate(s) {
  if (!s) return "";
  const dtFormat = new Intl.DateTimeFormat("default", {
    dateStyle: "short",
    timeStyle: "medium",
    hour12: false
  });

  return dtFormat.format(new Date(s));
}