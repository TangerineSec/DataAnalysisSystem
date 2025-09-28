<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <img src="cdn.authing.co/authing-fe-user-portal/2.31.2/favicon.ico" alt="Logo" v-if="logoExists">
          <i class="el-icon-data-analysis" v-else></i>
        </div>
        <h1>Excel 数据处理工具</h1>
        <p>专业的教育数据分析平台</p>
      </div>
      
      <div class="login-content">
        <div class="login-box">
          <h2>欢迎登录</h2>
          <p class="subtitle">使用您的账号登录系统</p>
          
          <div class="login-form">
            <el-button 
              type="primary" 
              size="large" 
              @click="handleLogin"
              class="login-btn"
              :loading="loading"
            >
              <i class="el-icon-user"></i>
              登录 / 注册
            </el-button>
            
            <div class="login-tips">
              <p><i class="el-icon-shield"></i> 安全认证由 Authing 提供</p>
              <p><i class="el-icon-info"></i> 首次登录将自动创建账号</p>
            </div>
            
            <div class="social-login" v-if="showSocialLogin">
              <div class="divider">
                <span>或使用以下方式登录</span>
              </div>
              
              <div class="social-buttons">
                <el-button 
                  circle 
                  size="medium"
                  @click="handleSocialLogin('wechat')"
                  class="social-btn wechat"
                >
                  <i class="el-icon-chat-dot-round"></i>
                </el-button>
                
                <el-button 
                  circle 
                  size="medium"
                  @click="handleSocialLogin('github')"
                  class="social-btn github"
                >
                  <i class="el-icon-link"></i>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 页脚 -->
    <div class="login-footer">
      <p>&copy; 2024 Excel数据处理工具. 由 Vue3 + Authing 强力驱动</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useGuard } from '@authing/guard-vue3'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  setup() {
    const guard = useGuard()
    const router = useRouter()
    const store = useStore()
    
    const loading = ref(false)
    const showSocialLogin = ref(true)
    const logoExists = ref(false)
    
    // 检查logo文件是否存在
    onMounted(() => {
      // 这里可以添加检查logo文件的逻辑
      logoExists.value = false // 默认设为false，实际项目中可以检查文件是否存在
      
      // 检查是否已经登录
      checkLoginState()
    })
    
    const checkLoginState = async () => {
      try {
        const loginState = await guard.getLoginState()
        if (loginState) {
          // 如果已经登录，直接跳转到首页
          await store.dispatch('login', {
            accessToken: loginState.accessToken,
            idToken: loginState.idToken,
            userInfo: loginState.userInfo
          })
          router.push('/')
        }
      } catch (error) {
        console.log('用户未登录或登录已过期')
      }
    }
    
    const handleLogin = async () => {
      loading.value = true
      
      try {
        // 启动登录弹窗
        await guard.start()
        
        // 监听登录成功事件
        guard.on('login', async (userInfo) => {
          console.log('登录成功:', userInfo)
          ElMessage.success('登录成功！')
          
          // 获取登录状态
          const loginState = await guard.getLoginState()
          if (loginState) {
            await store.dispatch('login', {
              accessToken: loginState.accessToken,
              idToken: loginState.idToken,
              userInfo: loginState.userInfo
            })
          }
          
          // 跳转到首页
          router.push('/')
        })
        
        // 监听登录失败事件
        guard.on('login-error', (error) => {
          console.error('登录失败:', error)
          ElMessage.error('登录失败，请重试')
          loading.value = false
        })
        
        // 监听登录框关闭事件
        guard.on('close', () => {
          loading.value = false
        })
        
      } catch (error) {
        console.error('登录过程出错:', error)
        ElMessage.error('登录过程出错，请重试')
        loading.value = false
      }
    }
    
    const handleSocialLogin = (provider) => {
      ElMessage.info(`${provider} 登录功能开发中...`)
    }
    
    return {
      loading,
      showSocialLogin,
      logoExists,
      handleLogin,
      handleSocialLogin
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
}

.login-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 1200px;
  margin: 20px;
  display: flex;
  min-height: 600px;
  overflow: hidden;
}

.login-header {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo i {
  font-size: 48px;
  color: white;
}

.login-header h1 {
  font-size: 32px;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.login-header p {
  font-size: 18px;
  margin: 0;
  opacity: 0.9;
}

.login-content {
  flex: 1;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-box {
  max-width: 400px;
  margin: 0 auto;
  width: 100%;
}

.login-box h2 {
  font-size: 28px;
  color: #333;
  margin: 0 0 10px 0;
  text-align: center;
}

.subtitle {
  color: #666;
  text-align: center;
  margin: 0 0 40px 0;
  font-size: 16px;
}

.login-form {
  text-align: center;
}

.login-btn {
  width: 100%;
  height: 50px;
  font-size: 18px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-btn i {
  margin-right: 8px;
}

.login-tips {
  color: #999;
  font-size: 14px;
  line-height: 1.8;
  margin-bottom: 30px;
}

.login-tips p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-tips i {
  margin-right: 6px;
  color: #409eff;
}

.social-login {
  margin-top: 20px;
}

.divider {
  position: relative;
  text-align: center;
  margin: 30px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e0e0e0;
  z-index: 1;
}

.divider span {
  background: white;
  padding: 0 15px;
  position: relative;
  z-index: 2;
  color: #999;
  font-size: 14px;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-btn {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.social-btn i {
  font-size: 20px;
}

.social-btn.wechat {
  background: #07c160;
  border-color: #07c160;
  color: white;
}

.social-btn.wechat:hover {
  background: #06ad56;
  border-color: #06ad56;
}

.social-btn.github {
  background: #333;
  border-color: #333;
  color: white;
}

.social-btn.github:hover {
  background: #555;
  border-color: #555;
}

.login-footer {
  text-align: center;
  color: white;
  margin-top: 30px;
  font-size: 14px;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    margin: 0;
    min-height: 100vh;
    border-radius: 0;
  }
  
  .login-header {
    padding: 40px 20px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
  
  .login-content {
    padding: 40px 20px;
  }
  
  .login-box {
    max-width: 100%;
  }
}
</style>
