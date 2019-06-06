<template>
    <label class="custom-toggle">
        <input @click.native="this.value=!this.value"
               type="checkbox"
               v-bind="$attrs"
               v-model="model">
        <span class="custom-toggle-slider rounded-circle"></span>
    </label>
</template>
<script>
    export default {
        name: "base-switch",
        inheritAttrs: false,
        props: {
            value: {
                type: Boolean,
                default: false,
                description: "Switch value"
            }
        },
        computed: {
            model: {
                get() {
                    return this.value;
                },
                set(value) {
                    this.$emit("input", value);
                }
            }
        }
    };
</script>
<style>
</style>
