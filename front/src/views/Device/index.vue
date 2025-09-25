<template>
  <div>
    <div class="crumbs">
    </div>
    <div class="container">
      <el-table :data="showTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="sn" label="序号" width="55" align="center"></el-table-column>
        <el-table-column prop="name" label="设备名"></el-table-column>
        <el-table-column prop="code" label="设备编码"></el-table-column>
        <el-table-column prop="ip" label="ip"></el-table-column>
        <el-table-column prop="rack" label="机架号"></el-table-column>
        <el-table-column prop="slot" label="卡槽号"></el-table-column>
        <el-table-column label="状态">
          <template #default="scope">
            <el-tag
                :type="`${scope.row.status === 'online'? 'success': 'danger'}`"
                effect="dark">
              {{scope.row.status === 'online'? '在线': '离线'}}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" align="center">

          <template #default="scope">
            <el-button type="text" icon="el-icon-view" @click="seePoint(scope.$index, scope.row)">详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
import {deviceListApi} from "@/api/device";

export default {
  name: "index",
  data() {
    return {
      showTableData: [],
      task: []
    }
  },
  methods: {
    getData() {
      deviceListApi().then(res => {
        this.showTableData = res
      })
    },
    seePoint(index, row) {
      this.$router.push({
        path: '/point',
        query: {
          deviceId: row.id,
          tagName: row.name + "-点位"
        }
      })
    }
  },
  mounted() {
    this.getData()
    this.task = []
    const task = setInterval(() => {
      this.getData()
    }, 2000)
    this.task.push(task)
  },
  beforeRouteLeave() {
    for(const task of this.task) {
      window.clearInterval(task);
    }
    this.task = []
  }
}
</script>

<style scoped>
</style>