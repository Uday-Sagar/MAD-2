<template>
  <div class="sidebar">
    <div class="user-section">
      <span class="user-name">Hello {{ userName }}</span>
    </div>
    <nav class="nav-links">
      <router-link :to="`/professional_home/${userId}`" class="nav-button">Home</router-link>
      <router-link :to="`/previous_services/${userId}`" class="nav-button">Previous Services</router-link>
      <router-link :to="`/professional_profile/${userId}`" class="nav-button">My Profile</router-link>
    </nav>
    <button class="logout-button" @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {    
name: 'ProfessionalNavBar',
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
