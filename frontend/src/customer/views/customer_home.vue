<template>
  <div class="cust-layout">
    <CustomerNavBar />
    <div class="cust-main-content">
      <h3><strong>Select a service to find professionals</strong></h3>
      
      <div class="service-grid">
        <div 
          v-for="service in services" 
          :key="service.id" 
          class="service-card" 
          @click="goToServiceProfessionals(service.type)">
          <h2>{{ service.type }}</h2>
          <p><strong>Price Range:</strong> {{ service.price_range }}</p>
          <p><strong>Duration:</strong> {{ service.duration }}</p>
          <p>{{ service.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
  name: 'CustomerHome',
  components: { CustomerNavBar },
  data() {
    return {
      services: []
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:7644/get_service_types');
        if (response.data.success) {
          this.services = response.data.services;
        } else {
          console.error('Failed to fetch services:', response.data.message);
        }
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    goToServiceProfessionals(serviceType) {
        const userId = this.$route.params.user_id; 
        this.$router.push({ 
            path: '/select_service_professional', 
            query: { serviceType, user_id: userId } 
        });
    }
  }
};
</script>

<style scoped>
.cust-main-content {
  padding: 20px;
  text-align: center;
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.service-card {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.service-card:hover {
  transform: scale(1.05);
}
</style>
