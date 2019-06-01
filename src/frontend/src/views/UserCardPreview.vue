<template>
    <div class="card card-profile shadow">
        <change-avatar :field="field"
                                    @crop-success="cropSuccess"
                                    @crop-upload-success="cropUploadSuccess"
                                    @crop-upload-fail="cropUploadFail"
                                    v-model="show"
                                    :width="300"
                                    :height="300"
                                    :url="url"
                                    langType='zh'
                                    img-format="png"
                                    :withCredentials='true'>
        </change-avatar>
        <div class="row justify-content-center">
            <div class="col-lg-3 order-lg-2">
                <div class="card-profile-image">
                    <a @click="toggleShow()">
                        <img :src="imgDataUrl" class="rounded-circle">
                    </a>
                </div>
            </div>
        </div>
        <div class="card-header text-center border-0 pt-8 pt-md-4 pb-0 pb-md-4">
            <div class="d-flex justify-content-between">
                <span class='description'>预览</span>
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
                <hr class="my-4" />
                <p>{{comment}}</p>
            </div>
        </div>
    </div>
</template>
<script>
    // import 'babel-polyfill'; // es6 shim
    import Upload from '@/plugins/vue-image-crop-upload/upload.vue';
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
            }
        }, 
        data() {
            return {
                show: false,
                field:'smfile',
                url: 'https://sm.ms/api/upload', 
                params: {
                },
                headers: {
                },
                imgDataUrl: 'img/theme/team-4-800x800.jpg', // the datebase64 url of created image
                friends_num: 0, 
                travel_groups_num: 0, 
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
             * [param] imgDataUrl
             * [param] field
             */
            cropSuccess(imgDataUrl, field){
                console.log('-------- crop success --------');
                this.imgDataUrl = imgDataUrl;
            },
            /**
             * upload success
             *
             * [param] jsonData  server api return data, already json encode
             * [param] field
             */
            cropUploadSuccess(jsonData, field){
                console.log('-------- upload success --------');
                console.log(jsonData);
                console.log('field: ' + field);
                this.imgDataUrl = jsonData.url;
            },
            /**
             * upload fail
             *
             * [param] status    server api return error status, like 500
             * [param] field
             */
            cropUploadFail(status, field){
                console.log('-------- upload fail --------');
                console.log(status);
                console.log('field: ' + field);
            }
        }
    }
</script>
