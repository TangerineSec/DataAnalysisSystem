<template>
  <div>
    <div class="crumbs">
    </div>
    <div class="container">
      <el-table :data="showTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="sn" label="序号" align="center"></el-table-column>
        <!--        <el-table-column prop="deviceName" label="设备"></el-table-column>-->
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="code" label="编码"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
        <el-table-column prop="type" label="类型"></el-table-column>
        <el-table-column label="时间" width="200">
            <template #default="scope">
              {{ codeToLatestValue[scope.row.code] ? codeToLatestValue[scope.row.code].time: null}}
            </template>
        </el-table-column>
        <!--        <el-table-column prop="valueTime" label="时间"></el-table-column>-->
        <el-table-column label="值">
                    <template #default="scope">
                      {{codeToLatestValue[scope.row.code] ? codeToLatestValue[scope.row.code].value : null}}
                    </template>

        </el-table-column>
        <!--        <el-table-column label="状态">-->
        <!--          <template #default="scope">-->
        <!--            <el-tag-->
        <!--                :type="`${scope.row.status === 'online'? 'success': 'danger'}`"-->
        <!--                effect="dark">-->
        <!--              {{scope.row.status === 'online'? '在线': '离线'}}-->
        <!--            </el-tag>-->
        <!--          </template>-->
        <!--        </el-table-column>-->

        <el-table-column label="操作" width="180" align="center">

          <template #default="scope">
            <el-button type="text" icon="el-icon-view" @click="seeCharts(scope.$index, scope.row)">数据探查
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog :title="showDialogName" v-model="showDataDialog" center style="position: relative">

        <div class="block"  style="position: absolute; left: 47%; transform: translate(-50%); z-index: 3">
          <el-date-picker
              v-model="selectTimeRange"
              type="datetimerange"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :default-time="selectTimeRange">
          </el-date-picker>
          <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        </div>
        <lineChart :x="x" :y="y" style="height:60vh"/>
<!--        <div ref="myChart" :style="{ height: '400px'}">-->
<!--        </div>-->
      </el-dialog>

    </div>

  </div>
</template>

<script>
import {pointListApi, pointValueTimeApi} from "@/api/point";
import {timestampToString} from "@/utils/utils";
import {getDataApi} from "@/api/iotData";
import * as echarts from 'echarts'
import lineChart from './line-chart'


export default {
  name: "index",
  components: {lineChart},
  data() {
    return {
      showTableData: [],
      showDataDialog: false,
      showDialogName: '',
      showPointCode: '',
      selectTimeRange: '',
      codeToLatestValue: {},
      charts: null,
      x: [],
      y: [],
      task: []
    }
  },
  methods: {
    getData() {
      const deviceId = this.$route.query.deviceId
      console.log('------------', deviceId);
      this.codeToLatestValue = {}
      let allCodeList = []
      this.removeTask()
      pointListApi(deviceId).then(res => {
        this.showTableData = res
        for (const point of res) {
          this.codeToLatestValue[point.code] = {
            time: point.valueTime,
            value: point.value
          }
          allCodeList.push(point.code)
        }
        const task = setInterval(() => {
          this.updateoPintValue(allCodeList)
        }, 1000)
        this.task.push(task)
      })
    },
    seeCharts(index, row) {
      this.showDataDialog = true
      this.$nextTick(() => {
        const now = new Date()
        const pastHour = new Date(new Date().setHours(now.getHours() - 1))
        // debugger
        this.selectTimeRange = [
          pastHour,
          now
        ]
        this.showPointCode = row.code
        this.showDialogName = `${row.deviceName}/${row.name}`
        this.search()
      })
    },
    search() {
      console.log(this.selectTimeRange)
      const start = timestampToString(this.selectTimeRange[0])
      const end = timestampToString(this.selectTimeRange[1])
      getDataApi(this.showPointCode, start, end).then(res => {
        this.drawLine(res)
      })

    },
    drawLine(data) {
      this.x = data.times
      this.y = data.values
      console.log('---------drawLine--------');
    },
    updateoPintValue(pointLit) {
      pointValueTimeApi({
        pointCodeList: pointLit
      }).then(res => {
        this.codeToLatestValue = res
      })
    },
    removeTask() {
      for (const task of this.task) {
        window.clearInterval(task);
      }
      this.task = []
    }
  },
  watch: {
    '$route.query.deviceId'() {
      if (this.$route.name !== 'point') {
        return
      }
      const deviceId = this.$route.query.deviceId
      this.getData(deviceId)
    }
  },
  mounted() {
    console.log('point mounted');
    this.getData()
  },
  beforeRouteLeave() {
    this.removeTask()
  }
}
</script>

<style scoped>
</style>