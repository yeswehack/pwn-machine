
import _ from "lodash";

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

function _mergeKeepShapeObject(dest, source) {
  const ret = {};
  Object.entries(dest).forEach(([key, destValue]) => {
      let sourceValue = source[key];
      if (typeof sourceValue !== "undefined") {
          ret[key] = mergeKeepShape(destValue, sourceValue);
      } else {
          ret[key] = destValue;
      }
  });
  return ret;
}

export function mergeKeepShape(dest, source) {
  if (_.isArray(dest)) {
    return source;
  } else if (_.isObject(dest)) {
      if (!_.isObject(source)) {
          return dest;
      }
      return _mergeKeepShapeObject(dest, source);
  } else {
      return source;
  }
}