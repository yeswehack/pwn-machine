export default {
    data: function () {
        return {
            message: 'hello',
            foo: 'abc',
            columns: [],
        }
    },
    computed: {
        columnsWithDelete() {
            return [...this.columns, {
                name: "delete",
                label: "Delete",
                align: "center",
                format: () => "×"
            }]
        }
    }
}


