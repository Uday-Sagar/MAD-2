<template>
  <div class="cust-sidebar">
      <div class="cust-user-section">
          <span class="user-name">Hello {{ userName }}</span>
      </div>
      <nav class="cust-nav-links">
          <router-link v-if="userId" :to="`/customer_home/${userId}`" class="cust-nav-button">Home</router-link>
          <router-link v-if="userId" :to="`/customer_service_requests/${userId}`" class="cust-nav-button">My Service Requests</router-link>
          <router-link v-if="userId" :to="`/rate_services/${userId}`" class="cust-nav-button">Rate services</router-link>
          <router-link v-if="userId" :to="`/customer_profile/${userId}`" class="cust-nav-button">My Profile</router-link>
      </nav>
      <button class="logout-button" @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CustomerNavBar',
  data() {
      return {
        userName: '', 
      };
  },
  computed: {
      userId() {
          return this.$route.params.user_id || this.$route.query.user_id;
      }
  },
  mounted() {
      this.fetchUserName();
  },
  methods: {
    async fetchUserName() {
        try {
            const response = await axios.get(`http://127.0.0.1:7644/get_user/${this.userId}`);
            if (response.data.success) {
                this.userName = response.data.user.name;
            } else {
                console.error("Failed to fetch user details:", response.data.message);
            }
        } catch (error) {
            console.error("Error fetching user details:", error);
        }
    },
    async logout() {
        try {
        console.log("Logging out...");
        } catch (error) {
        console.error("Logout error:", error);
        } finally {
        this.$router.push('/');
        }
    }
  }
};
</script>
