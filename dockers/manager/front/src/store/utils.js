
export function wrapLoading(f) {
    return async function (state, ...args) {
        state.dispatch("startLoading", null, { root: true })
        await f(state, ...args)
        state.dispatch("stopLoading", null, { root: true })
    }
}