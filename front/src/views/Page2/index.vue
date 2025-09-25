<template>
  <div>
    <div class="crumbs">
    </div>
    <div class="container">
      <div class="handle-box">

        <a href="https://musetransfer.com/s/1lktfah6c" target="_black"><el-button type="danger" icon="el-icon-upload" >点击模版下载:密码6156</el-button></a>
        <el-button type="success" icon="el-icon-upload" @click="handleAdd" style="margin: 0px 0px 0px 10px">选择Excel</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="filename1 !== '' && filename2 !== ''" @click="handleProcess">合并</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="exportFileName !== ''" @click="exportFile">导出</el-button>
      </div>
      <div style="margin: 50px auto; width: 200px"  v-show="showTableHeader2.length !== 0">平时成绩表格</div>

      <el-table :style="getTableContainStyle" empty-text="导入数据后显示" :data="showTableData1" border class="table" ref="multipleTable" header-cell-class-name="table-header" :fit="true">
        <el-table-column v-for="(d, index) in showTableHeader1" :prop=d.code :label="d.name"  align="center"></el-table-column>
      </el-table>

      <div style="margin: 50px auto; width: 200px ;  " v-show="showTableHeader2.length !== 0">终结成绩表格</div>

      <el-table :style="getTableContainStyle" empty-text="导入数据后显示" :data="showTableData2" border class="table" ref="multipleTable" header-cell-class-name="table-header" v-show="showTableHeader2.length !== 0" >
        <el-table-column v-for="(d, index) in showTableHeader2" :prop=d.code :label="d.name"  align="center"></el-table-column>
      </el-table>

            <div>
            <img style="width: 100%" src="@/assets/img/page2/tips.png">
            </div>
    </div>

    <!-- 编辑弹出框 -->
    <el-dialog title="点击方框或拖拽文件，可导入文件" v-model="diaLogShow"   width="30%">
      <el-form    >

        <el-form-item label="平时成绩" prop="file">
          <el-upload
              class="upload-import"
              ref="upload1"
              action=""
              :limit="1"
              :drag="true"
          :auto-upload="false">
          </el-upload>
        </el-form-item>

        <el-form-item label="终结成绩" prop="file">
          <el-upload
              class="upload-import"
              ref="upload2"
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

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "table",
  data() {
    return {
      diaLogShow: false,
      filename1: '',
      filename2: '',
      exportFileName: '',
      showTableData1: [],
      showTableHeader1: [
          { code: "date", name: "姓名" },
          { code: "date", name: "学号" },
          { code: "date", name:"SPOC成绩" },
          { code: "date", name: "雨课堂成绩（课前测，课中、课后测）" },
          { code: "date",  name: "PTA作业" },
          { code: "date", name: "PTA测试" },
          { code: "date", name: "project成绩" },
          { code: "date", name: "平时总成绩" },
          { code: "date", name: "终结性成" },
          { code: "date", name: "总评成绩" }
      ],
      showTableData2: [],
      showTableHeader2: [
          { code: "date", name: "姓名" },
          { code: "date", name: "学号" },
          { code: "date", name:"SPOC成绩" },
          { code: "date", name: "终结性成绩" },
      ],
    }
  },
    computed:{
      Tableheader1(){
      const maxVisibleHeaders = 10; // 控制前10列
      if (this.showTableHeader1.length <= maxVisibleHeaders){
        return this.showTableHeader1,this.showTableData2;
      } else {
        return this.showTableHeader1.slice(0,maxVisibleHeaders)
      }
    },
      getTableContainStyle(){ //控制函数
        if (this.showTableData2.length>0){
          return "height:100%";
        }else {
          return "height:240px;overflow-y=auto";
        }
      }
  },
  methods: {
    handleProcess(){
      // 处理excel
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
    exportFile() {
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/excel_export?filename=' + this.exportFileName
      window.open(url)
    },
    submit() {
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/upload_two_excel_and_preview'
      let formData = new FormData();
      const files1 = this.$refs.upload1.uploadFiles
      const files2 = this.$refs.upload2.uploadFiles
      if (files1.length === 0 || files2.length === 0) {
        alert('文件为空')
        return
      }
      let file1 = files1[0].raw
      let file2 = files2[0].raw
      formData.append('file2', file2)
      formData.append('file1', file1)
      console.log(url);
      // 添加请求头
      axios.post(url,formData,{
        'Content-type' : 'multipart/form-data'
      })
          .then(response => {
            console.log(response.data)
            if (response.data.code === 200) {
              this.showTableHeader1 =  response.data.data.data1.headers.slice(0)
              this.showTableData1 =  response.data.data.data1.data.slice(1)
              this.filename1 =  response.data.data.data1.filename.slice(0)

              this.showTableHeader2 =  response.data.data.data2.headers.slice(0)
              this.showTableData2 =  response.data.data.data2.data.slice(1)
              this.filename2 =  response.data.data.data2.filename.slice(0)

              this.exportFileName = ''
              this.$refs.upload1.uploadFiles = []
              this.$refs.upload2.uploadFiles = []
              this.diaLogShow = false

            } else {
              alert(response.data.msg)
            }
          })

    },

    handleAdd() {
      this.form = {}
      this.diaLogShow = true
      this.$refs.upload1.uploadFiles = []
      this.$refs.upload2.uploadFiles = []
    },
  },
  mounted() {
  }
}
</script>

<style scoped>
.container { /*page1_bg.png图片文件放置在Vue项目的静态资源目录中，引入背景*/
  background-image: url("~@/assets/img/page2/bg.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}

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
