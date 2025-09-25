<template>
  <div>
    <div class="crumbs">
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input v-model="kw" placeholder="搜索" class="handle-input mr10" @input="getFilterData"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="handleAdd">新建</el-button>
      </div>

      <el-table :data="showTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="sn" label="序号" width="55" align="center"></el-table-column>
        <el-table-column prop="roleShowName" label="角色名"></el-table-column>
        <el-table-column label="权限">
          <template #default="scope">
            <el-tag v-for="(item, i) in scope.row.permissionVoList"
                type="primary"
                disable-transitions>{{item.permissionShowName}}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" align="center">

          <template #default="scope">
            <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑
            </el-button>

            <el-button type="text" icon="el-icon-delete" class="red"
                       @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination background layout="total, prev, pager, next" :current-page="query.pageIndex"
                       :page-size="query.pageSize" :total="pageTotal" @current-change="handlePageChange"></el-pagination>
      </div>
    </div>

    <!-- 编辑弹出框 -->
    <el-dialog :title="`${createOrEdit === 'add'? '新建' : '编辑'}`" v-model="editVisible"   width="30%">
      <el-form label-width="70px"  :rules="rules" :model="form">
        <el-form-item label="角色名" prop="roleShowName">
          <el-input v-model="form.roleShowName"></el-input>
        </el-form-item>


        <el-form-item label="权限">
          <el-select v-model="form.permissionIds" placeholder="请选择" multiple>

            <el-option
                v-for="p in permissionList"
                :key="p.id"
                :label="p.permissionShowName"
                :value="p.id">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editVisible = false">取 消</el-button>
                    <el-button type="primary" @click="submit">确 定</el-button>
                </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from "element-plus";
import {fetchRoleList, fetchRoleWithPermissionVo, editRole, addRole, deleteRole} from "@/api/role";
import {pagination} from "@/utils/utils";
import {getAllPermission} from "@/api/permission";

export default {
  name: "table",
  data() {
    return {
      allData: [],
      filterData: [],
      showTableData: [],
      pageTotal: 0,
      kw: '',
      query: {
        pageSize: 15,
        pageIndex: 1
      },
      editVisible: false,
      createOrEdit: null, // add  或者  update
      form: {},
      permissionList:[],
    }
  },
  methods: {
    getData(){
      fetchRoleWithPermissionVo().then(res => {
        this.allData = res
        let sn = 1
        this.allData.map(item => {
          item.sn = sn
          sn ++
        })
        this.pageTotal = this.allData.length
        this.showTableData = pagination(this.query.pageIndex, this.query.pageSize, res)
        this.filterData = res
      })
    },
    handlePageChange(page) {
      this.query.pageIndex = page
      this.showTableData = pagination(this.query.pageIndex, this.query.pageSize, this.filterData)
    },
    handleDelete(index, row) {
      ElMessageBox.confirm("确定要删除吗？", "提示", {
              type: "warning",
            })
                .then(() => {
                  deleteRole({id: row.id}).then(res => {
                    ElMessage.success("删除成功");
                    this.getData()
                  })
                })
                .catch(() => {});
    },
    submit() {
      const callable = this.createOrEdit === 'add' ? addRole : editRole
      callable(this.form).then(res => {
        this.editVisible = false
        this.form = {}
        this.getData()
        ElMessage.success("成功");
      })
    },
    handleEdit(index, row) {
      this.createOrEdit = 'update'
      getAllPermission().then(res => {
        this.permissionList = res
      })
      this.editVisible = true
      this.form = JSON.parse(JSON.stringify(row));
      this.form.permissionIds = this.form.permissionVoList.map(permission => {
        return permission.id
      })
      console.log(this.form)
    },
    handleAdd() {
      this.form = {}
      this.createOrEdit = 'add'
      getAllPermission().then(res => {
        this.permissionList = res
      })
      this.editVisible = true
    },
    getFilterData() {
      const kw = this.kw
      this.filterData  = this.allData.filter(item => {
        return item.roleShowName.search(kw) !== -1
      })
      this.pageTotal = this.filterData.length
      this.showTableData = pagination(this.query.pageIndex, this.query.pageSize, this.filterData)
    }
  },
  mounted() {
    this.getData()
  }
}
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
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
</style>
