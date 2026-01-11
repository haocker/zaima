<template>
  <div class="setup-container">
    <div class="header">
      <div class="icon">⚙️</div>
      <h1 class="page-title">紧急联系人设置</h1>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label class="form-label">联系人姓名</label>
        <input
          class="form-input"
          v-model="contactForm.name"
          placeholder="请输入联系人姓名"
          confirm-type="done"
        />
      </div>

      <div class="form-group">
        <label class="form-label">联系人邮箱</label>
        <input
          class="form-input"
          v-model="contactForm.email"
          type="text"
          placeholder="请输入联系人邮箱"
          confirm-type="done"
        />
      </div>

      <div class="form-note">
        <div class="note-icon">💡</div>
        <div class="note-text">请确保邮箱地址正确，系统将在您连续多日未签到时发送邮件通知</div>
      </div>

      <button
        class="save-button"
        :disabled="!contactForm.name || !contactForm.email"
        @click="saveContact"
      >
        保存联系人
      </button>
    </div>

    <div class="current-contact" v-if="currentContact">
      <h2 class="section-title">
        <span class="icon">📋</span>
        当前联系人
      </h2>
      <div class="contact-card">
        <div class="contact-item">
          <text class="contact-icon">👤</text>
          <div class="contact-info">
            <text class="contact-label">姓名</text>
            <text class="contact-value">{{ currentContact.name }}</text>
          </div>
        </div>
        <div class="contact-item">
          <text class="contact-icon">📧</text>
          <div class="contact-info">
            <text class="contact-label">邮箱</text>
            <text class="contact-value">{{ currentContact.email }}</text>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../../utils/request';

export default {
  data() {
    return {
      contactForm: {
        name: '',
        email: ''
      },
      currentContact: null
    };
  },
  onLoad() {
    // 获取当前联系人信息
    this.getCurrentContact();
  },
  methods: {
    // 获取当前联系人
    async getCurrentContact() {
      try {
        const res = await request.get('/contact');
        if (res) {
          this.currentContact = res;
          // 填充表单
          this.contactForm.name = res.name || '';
          this.contactForm.email = res.email || '';
        }
      } catch (err) {
        console.error('获取联系人失败:', err);
        // 没有联系人时不报错
      }
    },
    
    // 保存联系人
    async saveContact() {
      try {
        // 验证表单
        if (!this.contactForm.name || !this.contactForm.email) {
          uni.showToast({
            title: '请填写完整信息',
            icon: 'none',
            duration: 2000
          });
          return;
        }
        
        // 保存联系人
        const res = await request.post('/contact', this.contactForm);
        
        // 更新当前联系人信息
        this.currentContact = res;
        
        // 显示成功提示
        uni.showToast({
          title: '保存成功',
          icon: 'success',
          duration: 2000
        });
      } catch (err) {
        console.error('保存联系人失败:', err);
        uni.showToast({
          title: '保存失败，请重试',
          icon: 'none',
          duration: 2000
        });
      }
    }
  }
};
</script>

<style scoped>
.setup-container {
  padding: 20px;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding-top: 20px;
}

.icon {
  font-size: 64px;
  margin-bottom: 15px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.form-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: block;
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  background-color: #fafafa;
  line-height: 48px;
}

.form-input:focus {
  border-color: #4CD964;
  background-color: #ffffff;
  box-shadow: 0 0 0 4px rgba(76, 217, 100, 0.1);
}

.form-note {
  display: flex;
  align-items: flex-start;
  background-color: #f0f9f0;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 25px;
  border-left: 4px solid #4CD964;
}

.note-icon {
  font-size: 20px;
  margin-right: 12px;
  flex-shrink: 0;
}

.note-text {
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.save-button {
  width: 100%;
  padding: 18px;
  font-size: 18px;
  font-weight: bold;
  background: linear-gradient(135deg, #4CD964 0%, #34C759 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 217, 100, 0.3);
}

.save-button:active {
  transform: translateY(2px);
  box-shadow: 0 2px 6px rgba(76, 217, 100, 0.3);
}

.save-button:disabled {
  background: linear-gradient(135deg, #cccccc 0%, #bbbbbb 100%);
  box-shadow: none;
  opacity: 0.6;
}

.current-contact {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title .icon {
  font-size: 28px;
  margin-right: 10px;
  margin-bottom: 0;
}

.contact-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 12px;
}

.contact-icon {
  font-size: 32px;
  margin-right: 15px;
  flex-shrink: 0;
}

.contact-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.contact-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 4px;
}

.contact-value {
  font-size: 16px;
  color: #333;
  font-weight: 600;
}
</style>