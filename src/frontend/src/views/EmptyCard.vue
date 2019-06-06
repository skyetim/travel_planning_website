<template>
    <div :class="type === 'dark' ? 'bg-default': ''"
         class="card shadow">
        <div :class="type === 'dark' ? 'bg-transparent': ''"
             class="card-header border-0">
            <div class="row align-items-center">
                <div class="col">
                    <h3 :class="type === 'dark' ? 'text-white': ''" class="mb-0">
                        {{title}}
                    </h3>
                </div>
                <div class='col text-right'>
                    {{message}}
                </div>
                <!-- <div class="col text-right">
                  <base-button type="primary" size="sm">See all</base-button>
                </div> -->
            </div>
        </div>


        <!-- <div class="card-footer d-flex justify-content-end"
             :class="type === 'dark' ? 'bg-transparent': ''">
          <base-pagination total="30"></base-pagination>
        </div> -->

    </div>
</template>
<script>
    export default {
        name: 'empty-card',
        props: {
            title: String,
            message: String
        },
        data() {
            return {}
        },
        methods: {}
    }
</script>
<style>
</style>
