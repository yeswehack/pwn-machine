const _ = require("lodash")
function _mergeKeepShapeArray(dest, source) {
  if (source.length != dest.length) {
      return dest;
  }
  return dest.map((v, i) =>  mergeKeepShape(v, source[i]))
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

function mergeKeepShape(dest, source) {
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

const value = {
  name: "toto",
  soa: {
    nameserver: "ns",
    ttl: [1,2,3],
  }
}

const definition = {
  name: '',
  soa: {
    nameserver: '',
    ttl: [1,2,3]
  }
}

 
const result = mergeKeepShape(definition, value);
console.log(definition)
console.log(result)