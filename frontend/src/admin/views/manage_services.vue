<template>
  <div class="admin-layout">
    <AdminNavBar />
    <div class="admin-main-content">
      <div class="header">
        <h2>Manage Services</h2>    
        <button class="add-service-button" @click="goToAddService">Add Service</button>
      </div>

      <table class="service-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Price Range</th>
            <th>Duration</th>
            <th>Description</th>
            <th>Options</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.Service_id">
            <td>{{ service.Service_id }}</td>
            <td>{{ service.Service_type }}</td>
            <td>{{ service.Price_range }}</td>
            <td>{{ service.Duration }}</td>
            <td>{{ service.Description }}</td>
            <td>
              <button class="edit-button" @click="goToEditService(service.Service_id)">Edit</button>
              <button class="delete-button" @click="deleteService(service.Service_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AdminNavBar from '@/admin/components/navbar.vue';

export default {
  name: "ManageServices",
  components: { AdminNavBar },
  data() {
    return {
      services: []
    };
  },
  methods: {
    goToAddService() {
      this.$router.push(`/add_services`);
    },
    goToEditService(serviceId) {
      this.$router.push(`/edit_service/${serviceId}`);
    },
    
    async fetchServices() {
      try {
        const token = localStorage.getItem("token"); 
        const response = await axios.get("http://127.0.0.1:7644/get_services", {
          headers: { Authorization: `Bearer ${token}` } // Remove Content-Type
        });
        if (response.data.success) {
          this.services = response.data.services;
        } else {
          console.error("Failed to fetch services:", response.data.message);
        }
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async deleteService(serviceId) {
      if (confirm("Are you sure you want to delete this service?")) {
        try {
          const token = localStorage.getItem("token"); // Retrieve JWT token
          const response = await axios.delete(`http://127.0.0.1:7644/delete_service/${serviceId}`, {
            headers: { Authorization: `Bearer ${token}` } // Include token in headers
          });
          if (response.data.success) {
            this.services = this.services.filter(service => service.Service_id !== serviceId);
          } else {
            console.error("Failed to delete service:", response.data.message);
          }
        } catch (error) {
          console.error("Error deleting service:", error);
        }
      }
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style>
.add-service-button {
margin-bottom: 10px;
padding: 8px 12px;
background-color: #4CAF50;
color: white;
border: none;
cursor: pointer;
}
.edit-button {
margin-right: 5px;
padding: 5px 10px;
background-color: #FFC107;
color: white;
border: none;
cursor: pointer;
}
.delete-button {
padding: 5px 10px;
background-color: #F44336;
color: white;
border: none;
cursor: pointer;
}
</style>
