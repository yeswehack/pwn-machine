import deepEqual from "deep-equal"
import deepcopy from "deepcopy"

export default {
    props: {
        value: { default: null },
    },
    data() {
        const formData = this.value === null ? this.createDefaultForm() : deepcopy(this.value)
        return { formData, originalData: null, internalEdit: false }
    },
    methods: {
        createDefaultForm() {
            return {}
        },
        renderFormData(v) {
            return v
        },
        clear() {
            this.formData = null
        },
        reset() {
            this.formData = deepcopy(this.originalData)
        },
        submit() {
            this.$emit("submit", this.formData)
        }
    },
    computed: {
        modified() {
            return !deepEqual(this.formData, this.originalData)
        }
    },
    watch: {
        value: {
            immediate: true,
            handler(value) {
                if (!this.internalEdit) {
                    this.originalData = value === null ? this.createDefaultForm() : deepcopy(value)
                }
            }
        },
        formData: {
            deep: true,
            async handler() {
                this.internalEdit = true
                await this.$emit("input", this.renderFormData(this.formData))
                this.internalEdit = false
            }
        }
    }
}