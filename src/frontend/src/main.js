import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import ArgonDashboard from './plugins/argon-dashboard'
import { Icon } from "leaflet";
import 'leaflet/dist/leaflet.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSession from 'vue-session';
import VueResource from 'vue-resource';
import md5 from 'js-md5';
import { backend } from './backend_config';
import Vuelidate from 'vuelidate';
import BootstrapVue from 'bootstrap-vue'
import moment from 'moment';
import {status, gender, gender_reverse} from './const';
import axios from 'axios';
import {backend as backend_conn} from './backendConnection';

Vue.use(BootstrapVue)
Vue.use(VueSession);
Vue.use(VueResource);
Vue.use(Vuelidate);
Vue.prototype.$gender = gender;
Vue.prototype.$gender_reverse = gender_reverse;
Vue.prototype.$axios = axios;
Vue.prototype.$backend_conn = backend_conn;
Vue.prototype.$md5 = md5;
Vue.prototype.$status = status;
Vue.prototype.$backend = backend;
Vue.prototype.compare = function (id) {
  return function (obj1, obj2) {
    if (obj1[id] < obj2[id]) {
      return -1;
    } else if (obj1[id] > obj2[id]) {
      return 1;
    } else {
      return 0;
    }
  };
}
Vue.prototype.newTravelGroup = function () {
  var travelGroupProto = {
    name: "新行迹",
    travel_group_id: null,
    travel_group_note: "",
    travel: [],
    dates: { start: "", end: "" },
    color:{hex: "#11cdef", a:0.8}
  };
  return travelGroupProto;
}

Vue.prototype.newTravel = function(){
  var travel = {
    location: "",
    coordinate: "",
    date_start: moment(Date()).format('YYYY-MM-DD'),
    date_end: moment(Date()).format('YYYY-MM-DD'),
    visibility: "P",
    vbool: false,
    city_id: null,
    travel_note: ""
  };
  return travel;
}

Vue.prototype.copy = function(obj) {
  let newObj = JSON.parse(JSON.stringify(obj));
  return newObj;
}
Vue.prototype.indexOf =  function(arr, el) {
  for (var i = 0; i < arr.length; ++i) {
    if (arr[i] == el) {
      return i;
    }
  }
},
Vue.config.silent = true;

Vue.http.options.emulateJSON = true;

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.config.productionTip = false

Vue.use(ArgonDashboard)

new Vue({
  router,
  render: h => h(App),
  created() {
    this.checkLogin();
  },
  methods: {
    checkLogin(){
      if (!this.$session.exists() && this.$route.name!='register') { // 如果没有login且不在register页自动跳转
        this.$router.push('/login');
      } else if (this.$session.exists() && (this.$route.name=='login' || this.$route.name=='register')){ // 如果已经login进入login页自动跳转
        this.$router.push('/');
      }
    }
  },
  watch: {
    '$route': 'checkLogin'
  }
}).$mount('#app')
