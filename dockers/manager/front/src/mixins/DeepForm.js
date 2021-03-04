export default {
    props: {
        value: { default: () => ({}) },
    },
    data() {
        return { formData: this.value }
    },
    methods: {
        renderFormData(v) {
            return v
        },
        clear() {
            this.formData = null
        }
    },
    watch: {
        formData: {
            deep: true,
            handler() {
                this.$emit("input", this.renderFormData(this.formData))
            }
        }
    }
}