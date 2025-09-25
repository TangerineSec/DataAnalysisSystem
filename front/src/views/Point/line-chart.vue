<template>
  <div class="full-width full-height">
    <div style="width: 100%; height: 100%;" ref="myChart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import {shallowRef} from "@vue/reactivity";
export default {
  data () {
    return {
      chart: null
    }
  },
  props: {
    x: {
      type: Array,
      default: () => []
    },

    y: {
      type: Array,
      default: () => []
    }
  },
  beforeUpdate () {
    this.clearChart()
  },
  mounted () {
    // return
    // this.setOption(this.x, this.y)
    // window.onresize = function () {
    //   this.resizeChart()
    // }.bind(this)
  },
  watch: {
    y (value) {
      this.setOption(this.x, this.y)
      console.log('watch' + this.y);


    }
  },
  methods: {
    resizeChart () {
      this.$nextTick(function () {
        this.chart && this.chart.resize()
      })
    },
    initChart () {
      if (!this.chart) {
        const chart = echarts.init(this.$refs['myChart'])
        this.chart = shallowRef(chart)
      }
    },
    setOption (x, y) {
      this.initChart()
      let option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            rotate: -20
          },
          data: x
        },
        grid: {
          top: 30,
          bottom: 80
        },
        yAxis: {
          type: 'value',
          min: 'dataMin',
          max: 'dataMax'
        },
        series: [{
          data: y,
          type: 'line'
        }]
      }
      if (x.length > 100) {
        option['dataZoom'] = [
          {
            type: 'slider',
            filterMode: 'filter',
            showDataShadow: false,
            bottom: 8,
            height: 10,
            borderColor: 'transparent',
            backgroundColor: '#aaa',
            handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z', // jshint ignore:line
            handleSize: 20,
            handleStyle: {
              shadowBlur: 6,
              shadowOffsetX: 1,
              shadowOffsetY: 2,
              shadowColor: '#aaa'
            },
            labelFormatter: ''
          }
        ]
      }
      const that = this
      const c = this.chart
      setTimeout(() => {
        c.setOption(option)
        that.resizeChart()
      }, 500)
    },
    clearChart () {
      if (this.chart) {
        this.chart.clear()
        this.chart = null
      }
    }
  }
}
</script>
