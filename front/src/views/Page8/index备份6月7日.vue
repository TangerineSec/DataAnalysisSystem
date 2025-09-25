<template>
  <div>

    <div class="crumbs">
    </div>
    <div class="container">


      <div class="handle-box">

        <a href="https://baidu.com" target="_black"><el-button type="danger" icon="el-icon-upload" >点击模版下载</el-button></a>
        <el-button type="success" icon="el-icon-upload" @click="handleAdd" style="margin: 0px 0px 0px 10px">选择Excel</el-button>
        <el-select placeholder="Sheet_name1" v-model="selectedSheet1" style="margin: 0px 0px 0px 10px">
          <el-option  v-for="(d, index) in sheet1" :label=d :value=d></el-option>
        </el-select>
        <el-select placeholder="主题" v-model="selectedTheme" style="margin: 0px 0px 0px 10px">
          <el-option  v-for="(d, index) in theme" :label=d :value=d></el-option>
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="handlePreview" style="margin: 0px 0px 0px 10px">先预览数据</el-button>
        <el-button type="primary" icon="el-icon-search" @click="handlePreviewCharts" style="margin: 0px 0px 0px 10px">再预览图片</el-button>


      </div>
      <div style="margin: 50px auto; width: 200px"  v-show="showTableHeader2.length !== 0">表格</div>
      <el-table :data="showTableData1" border class="table" ref="multipleTable" header-cell-class-name="table-header" :fit="true">
        <el-table-column v-for="(d, index) in showTableHeader1" :prop="d.code" :label="d.name"  align="center"></el-table-column>
      </el-table>

    </div>

    <!-- 编辑弹出框 -->
    <el-dialog title="点击方框或拖拽文件，可导入文件" v-model="diaLogShow"   width="30%">
      <el-form    >

        <el-form-item label="选择文件" prop="file">
          <el-upload
              class="upload-import"
              ref="upload1"
              action=""
              :limit="1"
              :drag="true"
              :auto-upload="false">
          </el-upload>
        </el-form-item>


      </el-form>
      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="diaLogShow = false">取 消</el-button>
                    <el-button type="primary" @click="submit">确 定</el-button>
                </span>
      </template>
    </el-dialog>
    <el-dialog v-model="showIframe"  width="90%" >
      <iframe :src="iframeUrl" frameborder="0" style="width: 100%; height: 700px">

      </iframe>
    </el-dialog>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "table",
  data() {
  // 使用 data 对象可以很方便地管理组件中所需的数据，并且能够保证组件的响应性能力
    return {
      showIframe: false,
      iframeUrl: '',
      diaLogShow: false,
      filename1: '',
      filename2: '',
      filename3: '',

      sheet1: [],
      sheet2: [],
      sheet3: [],
      selectedTheme: 'westeros',
      theme: [
        "light",
        "dark",
        "white",
        "chalk",
        "essos",
        "infographic",
        "macarons",
        "purple-passion",
        "roma",
        "romantic",
        "shine",
        "vintage",
        "walden",
        "westeros",
        "wonderland",
        "halloween",
      ],
      selectedSheet1: '',


      showTableData1: [],
      showTableHeader1: ['暂无数据'],
      showTableData2: [],
      showTableHeader2: ['暂无数据'],
      showTableData3: [],
      showTableHeader3: ['暂无数据'],
      exportFileName: '',
    }
  },
  methods: {
    handleProcess(){
      // 处理excel，用get提交一个请求。三个数组来分别存储三个表格的表头数据
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/merge?filename1=' + this.filename1 + '&filename2=' + this.filename2
      axios.get(url).then(response => {
        this.showTableHeader1 =  response.data.data.headers
        this.showTableData1 =  response.data.data.data
        this.showTableHeader2 = []
        this.showTableData2 = []
        this.filename =  ''
        this.exportFileName =  response.data.data.filename
      })

    },
    handlePreviewCharts() {
      //点击绑定的查看图片，这段代码的功能是在新窗口中打开一个URL
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/export_dimension_radar_chart?filename1='
          + this.filename1 + '&sheet1=' + this.selectedSheet1 + '&theme=' + this.selectedTheme
      window.open(url)
      return
      console.log('url :', url)
      this.showIframe = true
      this.iframeUrl = url

    },
    handlePreview() {
      //点击绑定的handlePreview，导入Excel可以查看数据
      if (this.sheet1 == '' ) {
        alert('请先选择sheet')
        return
      }
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/get_one_excel_data?filename1='
          + this.filename1 + '&sheet1=' + this.selectedSheet1
      console.log('url:', url)

      this.showTableData1 =  []
      this.showTableHeader1=[]
      axios.get(url,).then(response => {
        // 三个数组来分别存储三个表格的表头数据，使用方法：this.showTableHeader1 = response.data.data.headers;
        console.log(response.data.data.data1.data)
        this.showTableData1 =  response.data.data.data1.data.slice(1)
        this.showTableHeader1 =  response.data.data.data1.headers.slice(1)
          }
      )
    },
    submit() {
      //点击提交之后的函数处理
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/upload_file_and_get_sheet_name'
      let formData = new FormData();
      const files1 = this.$refs.upload1.uploadFiles
      if (files1.length === 0 ) {
        alert('文件为空')
        return
      }
      let file1 = files1[0].raw
      formData.append('file1', file1)
      console.log(url);
      // 添加请求头
      axios.post(url,formData,{
        'Content-type' : 'multipart/form-data'
      })
          .then(response => {
            console.log(response.data)
            if (response.data.code === 200) {
              // this.showTableHeader1 =  response.data.data.data1.headers
              // this.showTableData1 =  response.data.data.data1.data
              this.filename1 =  response.data.data.data1.filename
              this.sheet1 = response.data.data.data1.sheet

              this.exportFileName = ''
              this.$refs.upload1.uploadFiles = []
              this.diaLogShow = false

            } else {
              alert(response.data.msg)
            }
          })

    },

    handleAdd() {
      //点击选择Excel
      this.form = {}
      this.diaLogShow = true
      this.$refs.upload1.uploadFiles = []
    },
  },
  mounted() {
  }
}
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 300px;
  display: inline-block;
}
.table {
  width: 100%;
  font-size: 14px;
  height: 650px;
}
.red {
  color: #ff0000;
}
.mr10 {
  margin-right: 10px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>
