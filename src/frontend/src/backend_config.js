import { status } from './const';
import axios from 'axios';
import qs from 'qs';

export const backend = {
    remote: "http://139.162.123.242:9000/api/",

    response_handler: function (response, success, fail) {
        if (response.status === 200) {
            if (response.data.status == status["normal"]) {
                success(response);
            } else {
                fail(response);
            }
        }
    },

    err_handler: function (err) {
        console.log(err);
    },

    post_wrapper: function (api_name, data, success, fail) {
        return axios.post(this.remote + api_name, qs.stringify(data)).then(
            function (response) {
                backend.response_handler(response, success, fail);
            }
        ).catch(
            function (err) {
                backend.err_handler(err);
            })
    },

    get_all_travel_group_details: function (data, success, fail) {
        return backend.post_wrapper("get_all_travel_group_details", data, success, fail);
    },

    get_travel_group_list: function (data, success, fail) {
        return backend.post_wrapper("get_travel_group_list", data, success, fail);
    },

    get_travel_group_info: function (data, success, fail) {
        return backend.post_wrapper("get_travel_group_info", data, success, fail);
    },

    add_travel_group: function (data, success, fail) {
        return backend.post_wrapper("add_travel_group", data, success, fail);
    },

    set_travel_group_info: function (data, success, fail) {
        return backend.post_wrapper("set_travel_group_info", data, success, fail);
    },

    remove_travel_group: function (data, success, fail) {
        return backend.post_wrapper("remove_travel_group", data, success, fail);
    },

    get_travel_list: function (data, success, fail) {
        return backend.post_wrapper("get_travel_list", data, success, fail);
    },

    get_travel_info: function (data, success, fail) {
        return backend.post_wrapper("get_travel_info", data, success, fail);
    },
    set_travel_info: function (data, success, fail) {
        return backend.post_wrapper("set_travel_info", data, success, fail);
    },
    add_travel: function (data, success, fail) {
        return backend.post_wrapper("add_travel", data, success, fail);
    },
    remove_travel: function (data, success, fail) {
        return backend.post_wrapper("remove_travel", data, success, fail);
    },
    city_id_to_city: function (data, success, fail) {
        return backend.post_wrapper("city_id_to_city", data, success, fail);
    },

    address_to_city: function (data, success, fail) {
        return backend.post_wrapper("address_to_city", data, success, fail);
    },
}