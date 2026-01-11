<template>
  <div class="about-container">
    <div class="header">
      <div class="app-logo">
        <div class="logo-circle">
          <span class="logo-icon">👻</span>
        </div>
      </div>
      <h1 class="app-name">zaima</h1>
      <p class="app-slogan">让独处生活更安心</p>
      <p class="app-version">v1.0.0</p>
    </div>

    <div class="content">
      <div class="section">
        <h2 class="section-title">
          <span class="icon">💡</span>
          关于应用
        </h2>
        <p class="section-content">
          zaima 是为独居人群打造的轻量化安全工具，通过签到监测与紧急联络机制，构建无感化安全防护，让独处生活更安心。
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">
          <span class="icon">⚡</span>
          核心功能
        </h2>
        <div class="feature-list">
          <div class="feature-item">
            <div class="feature-icon">🔔</div>
            <div class="feature-text">
              <text class="feature-title">异常通知</text>
              <text class="feature-desc">连续多日未签到自动通知紧急联系人</text>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🚀</div>
            <div class="feature-text">
              <text class="feature-title">即开即用</text>
              <text class="feature-desc">无需注册，打开即可使用</text>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div class="feature-text">
              <text class="feature-title">隐私保护</text>
              <text class="feature-desc">加密存储，不收集无关权限</text>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">👥</div>
            <div class="feature-text">
              <text class="feature-title">适用广泛</text>
              <text class="feature-desc">适合所有独居人群</text>
            </div>
          </div>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">
          <span class="icon">🛡️</span>
          隐私政策
        </h2>
        <p class="section-content">
          我们采用加密技术保护您的紧急联系人信息与签到记录，拒绝收集位置等无关权限，从源头杜绝隐私泄露风险，确保个人信息安全无忧。
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">
          <span class="icon">📬</span>
          联系我们
        </h2>
        <p class="section-content">
          如有任何问题或建议，欢迎通过公众号与我们联系：
        </p>
        <div class="contact-email" @click="copyEmail">
          <text class="email-text">阿锤科技</text>
        </div>
      </div>
    </div>

    <div class="footer">
      <p class="copyright">© 2026 zaima. All rights reserved.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 页面数据
    };
  },
  methods: {
    // 复制邮箱
    copyEmail() {
      uni.setClipboardData({
        data: '阿锤科技',
        success: () => {
          uni.showToast({
            title: '已复制',
            icon: 'success',
            duration: 2000
          });
        }
      });
    }
  }
};
</script>

<style scoped>
.about-container {
  padding: 20px;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.content {
  width: 100%;
}

.header {
  text-align: center;
  margin-bottom: 40px;
  padding-top: 30px;
}

.logo-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CD964 0%, #34C759 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 8px 24px rgba(76, 217, 100, 0.3);
}

.logo-icon {
  font-size: 48px;
}

.app-name {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.app-slogan {
  font-size: 16px;
  color: #999;
  margin-bottom: 12px;
}

.app-version {
  font-size: 14px;
  color: #999;
  background-color: #e0e0e0;
  padding: 4px 12px;
  border-radius: 12px;
  display: inline-block;
}

.content {
  width: 100%;
}

.section {
  background-color: #ffffff;
  padding: 28px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title .icon {
  font-size: 28px;
  margin-right: 10px;
}

.section-content {
  font-size: 16px;
  color: #666;
  line-height: 1.7;
  margin-bottom: 0;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.feature-item:active {
  background-color: #f0f9f0;
}

.feature-icon {
  font-size: 32px;
  margin-right: 16px;
  flex-shrink: 0;
}

.feature-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.feature-desc {
  font-size: 14px;
  color: #999;
}

.contact-email {
  background: linear-gradient(135deg, #4CD964 0%, #34C759 100%);
  color: white;
  padding: 16px 24px;
  border-radius: 12px;
  text-align: center;
  margin-top: 16px;
  box-shadow: 0 4px 12px rgba(76, 217, 100, 0.3);
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.3s ease;
}

.contact-email:active {
  transform: translateY(2px);
  box-shadow: 0 2px 6px rgba(76, 217, 100, 0.3);
}

.email-text {
  font-size: 18px;
  font-weight: 600;
}

.copy-hint {
  font-size: 12px;
  opacity: 0.8;
}

.footer {
  margin-top: 40px;
  padding: 20px;
  text-align: center;
}

.copyright {
  font-size: 14px;
  color: #999;
}
</style>