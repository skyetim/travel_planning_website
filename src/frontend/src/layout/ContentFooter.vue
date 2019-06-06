<template>
    <footer class="footer px-4">
        <div class="row align-items-center justify-content-lg-between">
            <div class="col-lg-6">
                <div class="copyright text-center text-lg-left text-muted">
                    © {{year}} Final Project for Software Engineering, Group 1
                </div>
            </div>
        </div>
    </footer>
</template>
<script>
    export default {
        data() {
            return {
                year: new Date().getFullYear()
            };
        }
    };
</script>
<style></style>
