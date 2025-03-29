<template>
    <div class="cust-layout">
        <CustomerNavBar />
        <div class="cust-main-content">
            <h3><strong>Rate your services</strong></h3>

            <div v-if="loading" class="loading">Loading service requests...</div>
            <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
            <div v-else-if="serviceRequests.length === 0" class="no-requests">
                No services available for rating.
            </div>
            <div v-else class="service-requests">
                <table>
                    <thead>
                        <tr>
                            <th>Service Type</th>
                            <th>Professional</th>
                            <th>End Date</th>
                            <th>Action</th> <!-- New Column for Rating -->
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="service in serviceRequests" :key="service.id">
                            <td>{{ service.serviceType }}</td>
                            <td>{{ service.professionalName }}</td>
                            <td>{{ service.endDate }}</td>
                            <td>
                                <button 
                                    @click="rateService(service.id)" 
                                    class="rate-btn">
                                    Rate the Service
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
  name: 'CustomerServiceRatings',
  components: { CustomerNavBar },
  data() {
    return {
      userId: this.$route.params.user_id, 
      serviceRequests: [],
      loading: true,
      errorMessage: "" 
    };
  },
  mounted() {
    if (this.userId) {
      this.fetchCompletedServices();
    } else {
      console.error("User ID is missing in route params");
    }
  },
  methods: {
    async fetchCompletedServices() {
      try {
        const response = await axios.get(`http://127.0.0.1:7644/get_completed_service_requests/${this.userId}`);

        if (response.data.success) {
          this.serviceRequests = response.data.serviceRequests;
        } else {
          this.errorMessage = response.data.message;
          console.error('Failed to fetch service requests:', response.data.message);
        }
      } catch (error) {
        this.errorMessage = "Error fetching service requests.";
        console.error('Error fetching service requests:', error);
      } finally {
        this.loading = false;
      }
    },
    rateService(serviceId) {
        this.$router.push(`/submit_rating/${this.userId}/${serviceId}`);
    }
  }
};
</script>

<style scoped>
/* Table Styling */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

/* Buttons */
.rate-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.rate-btn:hover {
  background-color: #0056b3;
}

/* Loading and Error Messages */
.loading, .error, .no-requests {
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
}

.error {
  color: red;
}
</style>
