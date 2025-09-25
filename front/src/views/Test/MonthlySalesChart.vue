<template>
  <div>
<!--    <div class="field is-grouped">-->
<!--      <div class="control">-->
<!--        <label class="checkbox">-->
<!--          <input type="checkbox" :value="2018" v-model="selectedYears">-->
<!--          2018 Sales-->
<!--        </label>-->
<!--      </div>-->
<!--      <div class="control">-->
<!--        <label class="checkbox">-->
<!--          <input type="checkbox" :value="2017" v-model="selectedYears">-->
<!--          2017 Sales-->
<!--        </label>-->
<!--      </div>-->
<!--    </div>-->

    <line-chart
        :width="500"
        :height="300"
        :labels="['Jan', 'Feb', 'Mar', 'Apr', 'May']"
        :datasets="displayedDatasets"
        :options="$options.options"
    ></line-chart>
  </div>
</template>

<script>
import numeral from 'numeral';
import LineChart from './LineChart';
const datasets = {
  label: '2017 Sales',
      borderColor: 'rgba(49, 115, 220, 0.5)',
    backgroundColor: 'rgba(49, 115, 220, 0)',
    data: [299, 700, 450, 750, 450]
}
const options = {
  scales: {
    yAxes: [{
      ticks: {
        // beginAtZero: true,
        // callback: value => numeral(value).format('$0,0')
      }
    }]
  },
  tooltips: {
    mode: 'index',
    callbacks: {
      // label(tooltipItem, data) {
      //   const label = data.datasets[tooltipItem.datasetIndex].label;
      //   const value = numeral(tooltipItem.yLabel).format('$0,0');
      //   return `${label}: ${value}`;
      // }
    }
  }
};
export default {
  name: 'monthly-sales-chart',
  datasets,
  options,
  components: {
    LineChart
  },
  data() {
    return {
      selectedYears: [2018],
      // datasets: {
      //   label: '2017 Sales',
      //   borderColor: 'rgba(49, 115, 220, 0.5)',
      //   backgroundColor: 'rgba(49, 115, 220, 0)',
      //   data: [299, 700, 450, 750, 450]
      // }
    };
  },
  computed: {
    displayedDatasets() {
      return datasets
    }
  }
}
</script>
