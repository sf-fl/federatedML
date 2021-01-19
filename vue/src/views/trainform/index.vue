<template>
  <section class="user-edit">
    <n3-form
      ref="form"
      validate
    >
      <n3-form-item
        label="任务名"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          v-model="model.username"
          width="320px"
          :custom-validate="usernameValidate"
        >
        </n3-input>
      </n3-form-item>
      <n3-form-item
        label="数据集"
        need
        :label-col="3"
      >
        <input type="file" @change="inputFileChange">
        <n3-button @click.native="clicks" type="primary" size="mini" >上传</n3-button>
      </n3-form-item>
      <n3-form-item
        label="目标IP"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="ipValidate"
          v-model="model.ip"
          width="320px"
        >
        </n3-input>
      </n3-form-item>
      <n3-form-item
        label="目标端口"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="portValidate"
          v-model="model.port"
          width="320px"
        >
        </n3-input>
      </n3-form-item>
      <n3-form-item
        label="优先级"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          v-model="model.priority"
          width="320px"
          class="fl"
        >
        </n3-input>
        <div class="i-tips">
          默认 1
        </div>
      </n3-form-item>
      <n3-form-item
        label="学习类型"
        need
        :label-col="3"
      >
        <n3-select
          v-model="model.learningAlgorithm"
          width="160px"
        >
          <n3-option value="VLR">纵向逻辑回归</n3-option>
          <n3-option value="VSB">纵向SecureBoost</n3-option>
          <n3-option value="0">--敬请期待--</n3-option>

        </n3-select>
      </n3-form-item>
      <n3-form-item
        :label-col="3"
      >
        <n3-button
          @click.native="submit"
          type="primary"
          :loading="loading"
          class="submit-btn"
        >
          {{ loading ? '操作中' : '保存' }}
        </n3-button>
      </n3-form-item>
    </n3-form>
  </section>
</template>

<script>
  import API from '../../api'
  import qs from 'qs'
  import { mapState } from 'vuex'
  import { randomPassword, dateFormat } from '../../utils'
  // import submitfile from "xxxxxx"

  export default {
    computed: {
      ...mapState(['user'])
    },
    data () {
      return {
        model: {
          username: '',
          password: '',
          phone: '',
          ip: '',
          port: '',
          priority: 1,
          learningAlgorithm: '1',
          limitType: '1',
          cacheExpireTime: '24',
          expireDate: dateFormat(Date.now(), 'YYYY-MM-DD')
        },
        loading: false,
        files: ''
      }
    },
    methods: {
      reload () {
        // 重置表单
        this.model = {
          username: '',
          password: '',
          ip: '',
          port: '',
          phone: '',
          priority: 1,
          learningAlgorithm: 'VLR',
          limitType: '1',
          cacheExpireTime: '24',
          expireDate: dateFormat(Date.now(), 'YYYY-MM-DD')
        }
        this.loading = false
      },
      inputFileChange (e) {
        this.files = e.target.files[0]  // 当input中选择文件时触发一个事件并让data当中的files拿到所选择的文件
      },
      clicks () {
        if (!this.files) {
          console.print('请选择文件')
        } else {
        //   return
        //   let fd = new FormData ()
        //   fd.append('file',
        //   this.files
        // )
        //   submitfile(fd).then(res => {
        //   })
        }
      },
      // Random Pass
      randomPasswd () {
        this.model.password = randomPassword(18)
      },
      addTask () {
        let cond = Object.assign({}, this.model)
        // cond.expireDate = new Date(cond.expireDate).valueOf()
        this.loading = true
        this.$http.post(API.USER_ADD, qs.stringify(cond))
          .then(data => {
            this.loading = false
            this.n3Alert({
              content: '添加成功~',
              type: 'success',
              placement: 'top-right',
              duration: 2000,
              width: '240px' // 内容不确定，建议设置width
            })
            this.$router.push('/table/')
          })
          // eslint-disable-next-line handle-callback-err
          .catch(error => {
            this.loading = false
            this.n3Alert({
              content: '添加失败，请刷新重试~',
              type: 'danger',
              placement: 'top-right',
              duration: 2000,
              width: '240px' // 内容不确定，建议设置width
            })
          })
      },
      submit () {
        this.$refs.form.validateFields(result => {
          if (!result.isvalid) {
            return
          }
          return this.addTask()
        })
      },
      passwordValidate (val) {
        if (val && val.length > 5 && val.length < 19) {
          return {
            validStatus: 'success'
          }
        } else {
          return {
            validStatus: 'error',
            tips: '密码长度为6-18位'
          }
        }
      },
      ipValidate (val) {
        if (/^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$/.test(val)) {
          return {
            validStatus: 'success'
          }
        } else {
          return {
            validStatus: 'error',
            tips: '请输入正确的IP地址'
          }
        }
      },
      portValidate (val) {
        if (/^\d{1,5}$/.test(val)) {
          return {
            validStatus: 'success'
          }
        } else {
          return {
            validStatus: 'error',
            tips: '请输入正确端口'
          }
        }
      },
      usernameValidate (val) {
        if (val && val.length > 5 && val.length < 19) {
          return {
            validStatus: 'success'
          }
        } else {
          return {
            validStatus: 'error',
            tips: '账户名长度为6-18位'
          }
        }
      }
    },
    watch: {
      '$route' () {
        if (['trainForm'].indexOf(this.$route.name) > -1) {
          this.reload()
        }
      }
    },
    created () {
      this.reload()
    }
  }
</script>

<style lang="less">
  .user-edit {
    background: #fff;
    .submit-btn {
      width: 320px;
    }
    .refresh {
      cursor: pointer;
    }
    .i-tips {
      float: left;
      padding-left: 10px;
      color: #999;
    }
  }
</style>
