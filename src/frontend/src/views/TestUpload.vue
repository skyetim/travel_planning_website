<template>
    <div>
        <input @change="onFileChanged" type="file">
        <base-button @click="onUpload">Upload!</base-button>
    </div>
</template>
<script>
    export default {
        name: 'test',
        data() {
            return {
                selectedFile: null
            }
        },
        methods: {
            onFileChanged(event) {
                this.selectedFile = event.target.files[0]
            },
            onUpload() {
                // upload file, get it from this.selectedFile
                const formData = new FormData();
                formData.append('smfile', this.selectedFile, this.selectedFile.name);
                this.$axios.post('https://sm.ms/api/upload', formData).then(function (response) {
                    console.log(response)
                });
            }
        }
    }
</script>
