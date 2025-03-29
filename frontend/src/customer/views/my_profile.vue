<template>
  <div class="cust-layout">
    <CustomerNavBar />
    <div class="cust-main-content">
      <div v-if="loading">Loading profile...</div>
      <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>
      <div v-else-if="customer" class="profile-card">
        <div class="profile-header">
          <h2>{{ customer.name }}</h2>
        </div>
        <div class="profile-details">
          <p><strong>Email:</strong> {{ customer.email }}</p>
          <p><strong>Contact:</strong> {{ customer.contact || 'N/A' }}</p>
          <p><strong>City:</strong> {{ customer.city }}</p>
          <p><strong>Locality:</strong>{{ customer.locality }}</p>
        </div>
        <!-- Edit Profile Button -->
        <div class="edit-button-container">
          <button class="edit-button" @click="editProfile">Edit Profile</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CustomerNavBar from '@/customer/components/navbar.vue';
import axios from 'axios';

export default {
  name: 'CustomerProfile',
  components: { CustomerNavBar },
  data() {
    return {
      customer: null,
      loading: true,
      errorMessage: ''
    };
  },
  async created() {
    await this.fetchCustomerProfile();
  },
  methods: {
    async fetchCustomerProfile() {
      try {
        const userId = this.$route.params.user_id;
        if (!userId) {
          this.errorMessage = "User ID is missing in the route.";
          this.loading = false;
          return;
        }
        const response = await axios.get(`http://127.0.0.1:7644/get_customer_profile/${userId}`);
        if (response.data.success) {
          this.customer = response.data.data;
        } else {
          this.errorMessage = response.data.message || "Failed to fetch profile.";
        }
      } catch (error) {
        console.error("Error fetching profile:", error);
        this.errorMessage = "Error loading profile. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    editProfile() {
      const userId = this.$route.params.user_id;
      this.$router.push(`/edit_customer_profile/${userId}`);
    }
  }
};
</script>
