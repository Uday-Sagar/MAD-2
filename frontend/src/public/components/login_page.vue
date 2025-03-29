<template>
  <div class="main-body">
    <div class="form-container">
      <h4>Sign in to your account</h4>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input v-model="email" class="form-control" type="email" placeholder="Mail ID" required>
        </div>
        <br>
        <div class="form-group">
          <input v-model="password" class="form-control" type="password" placeholder="Password" required>
        </div>
        <br>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

        <button type="submit" class="btn btn-success" :disabled="loading || !email || !password">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
        <p style="margin-top:1rem;">New User?
          <button type="button" class="btn btn-primary" @click="navigateToSignup">Sign-up</button>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "LoginPage",
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      errorMessage: '',
    };
  },
  methods: {
    async handleSubmit() {
    if (this.loading) return;
    this.loading = true;
    this.errorMessage = '';

    try {
      const response = await axios.post('http://127.0.0.1:7644/login',
        {
          email: this.email,
          password: this.password
        },
        {
          withCredentials: true, // ✅ Ensures cookies are sent
        }
      );

      this.loading = false;

      if (response.data.success) {
        this.$router.push(response.data.redirect);
      } else {
        this.errorMessage = response.data.message || "Invalid credentials, please try again.";
      }
    } catch (error) {
      this.errorMessage = "Network error. Please check your connection and try again.";
      console.error('Error:', error);
      this.loading = false;
    }
  },
    navigateToSignup() {
      this.$router.push('/signup');
    }
  }
};
</script>
