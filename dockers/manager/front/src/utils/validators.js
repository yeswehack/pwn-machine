export function required(msg){
  return (v) => v ? undefined : msg
}

export function requiredArray(msg){
  return (v) => (Array.isArray(v) && v.length) ? undefined : msg
}
