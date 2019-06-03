import Badge from "../components/Badge";
import BaseAlert from "../components/BaseAlert";
import BaseButton from "../components/BaseButton";
import BaseCheckbox from "../components/BaseCheckbox";
import BaseInput from "../components/BaseInput";
import BaseDropdown from "../components/BaseDropdown";
import BaseNav from "../components/BaseNav";
import BasePagination from "../components/BasePagination";
import BaseProgress from "../components/BaseProgress";
import BaseRadio from "../components/BaseRadio";
import BaseSlider from "../components/BaseSlider";
import BaseSwitch from "../components/BaseSwitch";
import BaseTable from "../components/BaseTable";
import BaseHeader from "../components/BaseHeader";
import BeautInput from "../components/BeautInput";
import Card from "../components/Card";
import Draggable from "../components/Draggable";
import Editable from "../components/Editable";
import StatsCard from "../components/StatsCard";
import Modal from "../components/Modal";
import TabPane from "../components/Tabs/TabPane";
import Tabs from "../components/Tabs/Tabs";
import TravelStats from "../components/TravelStats";
import EditableProjectsTable from "../views/Tables/EditableProjectsTable"
import swatches from "vue-color/src/components/Swatches.vue";

export default {
  install(Vue) {
    Vue.component(Badge.name, Badge);
    Vue.component(BaseAlert.name, BaseAlert);
    Vue.component(BaseButton.name, BaseButton);
    Vue.component(BaseInput.name, BaseInput);
    Vue.component(BaseNav.name, BaseNav);
    Vue.component(BaseDropdown.name, BaseDropdown);
    Vue.component(BaseCheckbox.name, BaseCheckbox);
    Vue.component(BasePagination.name, BasePagination);
    Vue.component(BaseProgress.name, BaseProgress);
    Vue.component(BaseRadio.name, BaseRadio);
    Vue.component(BaseSlider.name, BaseSlider);
    Vue.component(BaseSwitch.name, BaseSwitch);
    Vue.component(BaseTable.name, BaseTable);
    Vue.component(BaseHeader.name, BaseHeader);
    Vue.component(BeautInput.name, BeautInput);
    Vue.component(Card.name, Card);
    Vue.component(Draggable.name, Draggable);
    Vue.component(Editable.name, Editable);
    Vue.component(EditableProjectsTable.name, EditableProjectsTable);
    Vue.component(StatsCard.name, StatsCard);
    Vue.component(Modal.name, Modal);
    Vue.component(TabPane.name, TabPane);
    Vue.component(Tabs.name, Tabs);
    Vue.component(TravelStats.name, TravelStats);
    Vue.component('swatches', swatches);
  }
};
