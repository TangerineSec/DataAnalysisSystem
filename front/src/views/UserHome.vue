<template>
    <div class="about">
        <v-header headerName="学习成效分析可视化系统免费版" style="font-size: 22px;color: black"/>
        <v-sidebar :items="items"/>
        <div class="content-box" :class="{ 'content-collapse': collapse }" style="background: linear-gradient(to right, #90cdf4, #a7f3d0);">
            <v-tags></v-tags>
            <div class="content" style="background: linear-gradient(to right, #90cdf4, #a7f3d0);width: 100%; height: 100%; border-radius: 1rem; ">
              <keep-alive>
                <router-view v-slot="{ Component }">
                    <transition name="move" mode="out-in">
                        <keep-alive :include="tagsList">
                            <component :is="Component" />
                        </keep-alive>
                    </transition>
                </router-view>
                </keep-alive>
                <!-- <el-backtop target=".content"></el-backtop> -->
            </div>
        </div>
    </div>
</template>
<script>
import { computed } from "vue";
import { useStore } from "vuex";
import vHeader from "../components/Header.vue";
import vSidebar from "../components/Sidebar.vue";
import vTags from "../components/Tags.vue";
export default {
    components: {
        vHeader,
        vSidebar,
        vTags,
    },
    setup() {
        const store = useStore();
        const tagsList = computed(() =>
            store.state.tagsList.map((item) => item.name)
        );
        const collapse = computed(() => store.state.collapse);
        // 这是加左侧菜单的
        const items = [
          {
            icon: "el-icon-lx-cascades",
            index: "/",
            title: "1.加权计算功能",
          },
          {
            icon: "el-icon-lx-cascades",
            index: "/page2",
            title: "2.合并Excel功能",
          },
          {
            icon: "el-icon-lx-cascades",
            index: "/page3",
            title: "3.折线图功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page4",
            title: "4.柱状图功能",
          },
           {
            icon: "el-icon-lx-cascades",
            index: "/page5",
            title: "5.雨课堂功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page6",
            title: "6.饼状图功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page7",
            title: "7.归一化成绩功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page8",
            title: "8.能力维度图功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page9",
            title: "9.年得分率散点图功能",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page10",
            title: "10.SPOC雷达图",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page11",
            title: "11.自定义SPOC雷达图",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page12",
            title: "12.基础归一化图",
          },
            {
            icon: "el-icon-lx-cascades",
            index: "/page13",
            title: "13.升级归一化图",
          },// 在此处增加后会在网页上显示增加的标题
          //   {
          //   icon: "el-icon-lx-cascades",
          //   index: "/page13",
          //   title: "13.年等级评估功能",
          // },
          //   {
          //   icon: "el-icon-lx-cascades",
          //   index: "/page5",
          //   title: "5.雨课堂功能",
          // },
        ]

      return {
        tagsList,
        collapse,
        items
        };
    },
};
</script>
