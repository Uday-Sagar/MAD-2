<template>
  <div class="admin-sidebar">
    <div class="admin-user-section">
      <span class="user-name">{{ userName }}</span>
    </div>
    <nav class="admin-nav-links">
      <router-link :to="`/admin_home`" class="admin-nav-button">Admin Dashboard</router-link>
      <router-link :to="`/service_professional_request`" class="admin-nav-button">
        Service Professional Request
      </router-link>
      <router-link :to="`/manage_customers`" class="admin-nav-button">Manage Customers</router-link>
      <router-link :to="`/manage_service_professionals`" class="admin-nav-button">Manage Service Professionals</router-link>
      <router-link :to="`/manage_services`" class="admin-nav-button">Manage Services</router-link>
    </nav>
    <button class="admin-logout-button" @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {    
name: 'AdminNavBar',
data() {
  return {
    userName: 'John Doe', 
  };
},

methods: {
  async logout() {
    try {
      console.log("Logging out...");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      localStorage.removeItem('admin_id');
      this.$router.push('/');
    }
  }
}
};
</script>
