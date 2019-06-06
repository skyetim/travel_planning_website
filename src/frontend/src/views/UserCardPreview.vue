<template>
    <div class="card card-profile shadow">
        <change-avatar :field="field"
                       :height="300"
                       :url="url"
                       :width="300"
                       :withCredentials='true'
                       @crop-success="cropSuccess"
                       @crop-upload-fail="cropUploadFail"
                       @crop-upload-success="cropUploadSuccess"
                       img-format="png"
                       langType='zh'
                       v-model="show">
        </change-avatar>
        <div class="row justify-content-center">
            <div class="col-lg-3 order-lg-2">
                <div class="card-profile-image">
                    <a @click="toggleShow()" title="点击以更改头像" v-b-tooltip.hover.top>
                        <img :src="avatar_url" class="rounded-circle">
                    </a>
                </div>
            </div>
        </div>
        <div class="card-header text-center border-0 pt-8 pt-md-4 pb-0 pb-md-4">
            <div class="d-flex justify-content-between">
                <span class='description' v-if="preview">预览</span>
                <!-- <base-button size="sm" type="info" class="mr-4">Connect</base-button> -->
                <!-- <base-button size="sm" type="default" class="float-right">Message</base-button> -->
            </div>
        </div>
        <div class="card-body pt-0 pt-md-4">
            <div class="row">
                <div class="col">
                    <div class="card-profile-stats d-flex justify-content-center mt-md-5">
                        <div>
                            <span class="heading">{{friends_num}}</span>
                            <span class="description">朋友</span>
                        </div>
                        <div>
                            <span class="heading">{{travel_groups_num}}</span>
                            <span class="description">行迹</span>
                        </div>
                        <!-- <div>
                            <span class="heading">89</span>
                            <span class="description">Comments</span>
                        </div> -->
                    </div>
                </div>
            </div>
            <div class="text-center">
                <h3>
                    {{user_name}}<span class="font-weight-light">, {{gender}}</span>
                </h3>
                <div class="h5 font-weight-300">
                    <i class="ni location_pin mr-2"></i>{{resident_city}}
                </div>
                <!-- <div class="h5 mt-4">
                    <i class="ni business_briefcase-24 mr-2"></i>Solution Manager - Creative Tim Officer
                </div>
                <div>
                    <i class="ni education_hat mr-2"></i>University of Computer Science
                </div> -->
                <hr class="my-4"/>
                <p>{{comment}}</p>
            </div>
        </div>
    </div>
</template>
<script>
    // import 'babel-polyfill'; // es6 shim
    import Upload from '@/plugins/vue-image-crop-upload/upload.vue';
    import BTooltipDirective from 'bootstrap-vue/es/directives/tooltip'

    export default {
        name: 'user_card_preview',
        props: {
            user_name: {
                'default': '未设置'
            },
            gender: {
                'default': '未设置'
            },
            resident_city: {
                'default': '未设置'
            },
            comment: {
                'default': '未设置'
            },
            avatar_url: {
                'default': 'img/theme/team-4-800x800.jpg'
            },
            preview: {
                'default': false,
                'description': 'Whether is a preview user card. '
            }
        },
        mounted() {
            this.get_friends_num();
            this.get_travel_groups_num();
        },
        directives: {
            'b-tooltip': BTooltipDirective
        },
        data() {
            return {
                show: false,
                field: 'smfile',
                url: 'https://sm.ms/api/upload',
                params: {},
                headers: {},
                friends_num: 0,
                travel_groups_num: 0
            }
        },
        components: {
            'change-avatar': Upload
        },
        methods: {
            toggleShow() {
                this.show = !this.show;
            },
            /**
             * crop success
             *
             * [param] avatar_url
             * [param] field
             */
            cropSuccess(avatar_url, field) {
                console.log('-------- crop success --------');
            },
            /**
             * upload success
             *
             * [param] jsonData  server api return data, already json encode
             * [param] field
             */
            cropUploadSuccess(jsonData, field) {
                console.log('-------- upload success --------');
                var that = this;

                function success(response) {
                    that.$router.go();
                }

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

                this.$backend_conn('set_user_avatar_url', {avatar_url: jsonData.url}, that, success, fail);
            },
            /**
             * upload fail
             *
             * [param] status    server api return error status, like 500
             * [param] field
             */
            cropUploadFail(status, field) {
                console.log('-------- upload fail --------');
                console.log(status);
                console.log('field: ' + field);
            },
            get_friends_num() {
                var that = this;

                function success(response) {
                    that.friends_num = response.data.count;
                }

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

                this.$backend_conn('get_friend_list', {}, that, success, fail);
            },
            get_travel_groups_num() {
                var that = this;

                function success(response) {
                    that.travel_groups_num = response.data.count;
                }

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

                this.$backend_conn('get_travel_group_list', {}, that, success, fail);
            }
        }
    }
</script>
