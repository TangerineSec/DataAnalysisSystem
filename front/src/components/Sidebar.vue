<template>
    <div class="sidebar" >
<!--      侧边颜色更改  background-color="#ffe5e5" style="background-color:black"-->
        <el-menu class="sidebar-el-menu" :default-active="onRoutes" :collapse="collapse" style="background: linear-gradient(to top, #90cdf4, #a7f3d0);"
            text-color="#bfcbd9" active-text-color="black" unique-opened router>
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index">
                        <template #title >
                            <i :class="item.icon"></i>
                            <span>{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index">
                                <template #title>{{ subItem.title }}</template>
                                <el-menu-item v-for="(threeItem, i) in subItem.subs" :key="i" :index="threeItem.index">
                                    {{ threeItem.title }}</el-menu-item>
                            </el-submenu>
                            <el-menu-item v-else :index="subItem.index" :key="subItem.index">{{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item v-if="item.title" :index="item.index" :key="item.index" style="color: black;font-size: 18px">
                        <i :class="item.icon"></i>
                        <template #title>{{ item.title }}</template>
                    </el-menu-item>
                  <el-divider v-else-if="!item.title && !collapse" style="background-color: #444; height: 5px; margin: 1px 0"></el-divider>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
import { computed, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import {toRefs} from "@vue/reactivity";

export default {
    props: {
      items: Array
    },
    setup(props, { emit, attrs, slots }) {
        const {items} = toRefs(props)

        const route = useRoute();

        const onRoutes = computed(() => {
            return route.path;
        });

        const store = useStore();
        const collapse = computed(() => store.state.collapse);

        return {
            items,
            onRoutes,
            collapse,
        };
    },
};
</script>

<style scoped>
.sidebar {
    display: block;
    position: absolute;
    width: 100%;
    left: 0;
    top: 70px;
    bottom: -20px;/* 底部颜色距离*/
    overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
    width: 0px;
}
.sidebar-el-menu:not(.el-menu--collapse) {
    width: 100%;
    /*background-color: #f02d2d;*/
}
.sidebar > ul {
    height: 100%;
}
</style>
